"""Command-line interface."""
import ast
import sys
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

import click
import shapely

from .nldi_xstool import getxsatendpts
from .nldi_xstool import getxsatpathpts
from .nldi_xstool import getxsatpoint

# from typing import List

# 3dep resolution
resdict = {"1m": 1.0, "3m": 3.0, "5m": 5.0, "10m": 10.0, "30m": 30.0, "60m": 60.0}

# from:
# https://gis.stackexchange.com/questions/363221/
# how-do-you-validate-longitude-and-latitude-coordinates-in-python/378885#378885


def valid_lonlat(
    ctx: click.Context, param: click.core.Option, value: Tuple[float, float]
) -> Tuple[float, float]:
    """This validates a lat and lon.

    This validates a lat and lonpoint can be located
    in the bounds of the WGS84 CRS, after wrapping the
    longitude value within [-180, 180).

    :param lon: a longitude value
    :param lat: a latitude value
    :return: (lon, lat) if valid, None otherwise
    """
    # print(f"latlon: {param, value}")

    lon = float(value[0])
    lat = float(value[1])
    # Put the longitude in the range of [0,360):
    lon %= 360
    # Put the longitude in the range of [-180,180):
    if lon >= 180:
        lon -= 360
    lon_lat_point = shapely.geometry.Point(lon, lat)
    lon_lat_bounds = shapely.geometry.Polygon.from_bounds(
        xmin=-180.0, ymin=-90.0, xmax=180.0, ymax=90.0
    )
    # return lon_lat_bounds.intersects(lon_lat_point)
    # would not provide any corrected values
    if lon_lat_bounds.intersects(lon_lat_point):
        return lon, lat
        # return lon, lat
    # except ValueError:
    msg = f"Not valid lon lat pair: {lon, lat}"
    print(msg)
    raise click.BadParameter(msg)


class NLDIXSTool:
    """Simple class to handle global crs."""

    def __init__(self: "NLDIXSTool") -> None:
        """Init NLDIXSTool."""
        self.out_crs = "epsg:4326"

    def setoutcrs(self: "NLDIXSTool", out_crs: str = "epsg:4326") -> None:
        """Set the CRS for output.

        Args:
            out_crs (str): Set the CRS string for projection of output. Defaults to "epsg:4326".
        """
        self.out_crs = out_crs

    def outcrs(self: "NLDIXSTool") -> str:
        """Get the output CRS.

        Returns:
            str: The epsg crs code.
        """
        return self.out_crs

    def __repr__(self: "NLDIXSTool") -> str:
        """Representation.

        Returns:
            str: Representation ouput.
        """
        return f"NLDI_XSTool {self.out_crs}"


# Common options
pass_nldi_xstool = click.make_pass_decorator(NLDIXSTool)
res_opt = click.option(
    "-r",
    "--resolution",
    type=click.Choice(["1m", "3m", "5m", "10m", "30m", "60m"], case_sensitive=False),
    default="10m",
    help=(
        "Resolution of DEM used.  "
        "Note: 3DEP provides server side interpolatin given best available data"
    ),
)
file_opt = click.option(
    "-f",
    "--file",
    default=None,
    type=str,
    help="enter path and filename for json ouput: path/to/file.json",
)
verb_opt = click.option("-v", "--verbose", is_flag=True, help="verbose ouput")
npts_opt = click.option(
    "-n", "--numpoints", default=100, type=int, help="number of points in cross-section"
)


@click.group()
@click.option(
    "--outcrs",
    default="epsg:4326",
    help="Projection CRS to return cross-section geometry: default is epsg:4326",
)
@click.version_option("0.1")
@click.pass_context
def main(ctx: Any, outcrs: str) -> None:
    """nldi-xstool is a command line tool to for elevation-based services to the NLDI."""
    ctx.obj = NLDIXSTool()
    ctx.obj.setoutcrs(outcrs)


# XS command at point with NHD
@main.command()
@click.option(
    "-ll",
    "--lonlat",
    required=True,
    nargs=2,
    type=float,
    callback=valid_lonlat,  # type: ignore
    help="format lon,lat (x,y) as floats for example: -103.8011 40.2684",
)
@click.option(
    "-w", "--width", default=1000.0, type=float, help="width of cross-section"
)
@file_opt
@npts_opt
@res_opt
@verb_opt
@pass_nldi_xstool
def xsatpoint(
    nldi_xstool: "NLDIXSTool",
    lonlat: Tuple[float, float],
    numpoints: int,
    width: float,
    resolution: str,
    verbose: bool,
    file: str = "",
) -> None:
    """Topographic cross-section at user-defined point.

    This function relies on the U.S. Geological Survey's NLDI and 3DEP program elevation
    services to return a topographic cross-section, at nearest NHD stream-segment
    based on user-defined point, width, number of points, and 3DEP spatial resolution.

    NOTE: 3DEP does not specifically include bathymetry.
    """
    x, y = lonlat
    if verbose:
        print(
            "\n".join(
                [
                    "input:",
                    f"lonlat: {lonlat}",
                    f"lon: {x}, lat: {y}",
                    f"npts: {numpoints}",
                    f"width: {width}",
                    f"resolution: {resolution}",
                    f"crs: {nldi_xstool.outcrs()}",
                    f"file: {file}",
                    f"out_epsg: {nldi_xstool.outcrs()}",
                ]
            )
        )
    xs = getxsatpoint(
        point=lonlat,
        numpoints=numpoints,
        width=width,
        file=file,
        res=resdict[resolution],
    )

    if file != "":
        print(xs.to_json())


# XS command at user defined endpoints


@main.command()
@click.option(
    "-s",
    "--startpt",
    required=True,
    type=tuple((float, float)),
    help="format x y pair as floats for example: -103.801134 40.267335",
)
@click.option(
    "-e",
    "--endpt",
    required=True,
    type=tuple((float, float)),
    help="format x y pair as floats for example: -103.800787 40.272798 ",
)
@click.option(
    "-c",
    "--crs",
    required=True,
    type=str,
    help="spatial reference of input data",
    default="epsg:4326",
)
@file_opt
@npts_opt
@res_opt
@verb_opt
@pass_nldi_xstool
def xsatendpts(
    nldi_xstool: "NLDIXSTool",
    startpt: Tuple[float, float],
    endpt: Tuple[float, float],
    crs: str,
    numpoints: int,
    resolution: str,
    file: Optional[str],
    verbose: bool,
) -> None:
    """Topographic cross-section at user-defined end points.

    This function relies on the U.S. Geological Survey's 3DEP program elevation services
    to return a topographic cross-section based on user-defined end-points, number of
    points, and 3DEP spatial resolution.

    NOTE: 3DEP does not specifically include bathymetry.
    """
    x1, y1 = startpt
    x2, y2 = endpt
    if verbose:
        print(
            "\n".join(
                [
                    "input:",
                    f"start: {startpt}",
                    f"end: {endpt}",
                    f"x1: {x1}, y1: {y1}",
                    f"x2: {x2}, y2: {y2}",
                    f"npts: {numpoints}",
                    f"resolution: {resolution}",
                    f"input_crs:  {crs}",
                    f"output_crs: {nldi_xstool.outcrs()}",
                    f"file: {file}",
                    f"verbose: {verbose}",
                ]
            )
        )
    path = [startpt, endpt]
    xs = getxsatendpts(
        path=path, numpts=numpoints, res=resdict[resolution], crs=crs, file=file
    )
    if file is None:
        print(xs.to_json())


# XS command at user defined path
@main.command()
@click.argument("path")
@click.option(
    "-c",
    "--crs",
    required=True,
    type=str,
    help="spatial reference of input data",
    default="epsg:4326",
)
@file_opt
@npts_opt
@res_opt
@verb_opt
@pass_nldi_xstool
def xsatpathpts(
    nldi_xstool: "NLDIXSTool",
    path: List[Tuple[float, float]],
    crs: str,
    numpoints: int,
    resolution: str,
    file: Optional[str],
    verbose: bool,
) -> None:
    """Topographic cross-section at user-defined end points.

    This function relies on the U.S. Geological Survey's 3DEP program elevation services
    to return a topographic cross-section based on user-defined end-points, number of
    points, and 3DEP spatial resolution.

    NOTE: 3DEP does not specifically include bathymetry.
    """
    t_path = ast.literal_eval(path)
    for pt in t_path:
        print(pt[0], pt[1])
    if verbose:
        print(
            "\n".join(
                [
                    "input:",
                    f"path:{t_path} ",
                    f"path type: {type(t_path)}",
                    # [f"{(pnt[0], pnt[1]), }" for pnt in t_path],
                    f"npts: {numpoints}",
                    f"resolution: {resolution}",
                    f"input_crs:  {crs}",
                    f"output_crs: {nldi_xstool.outcrs()}",
                    f"file: {file}",
                    f"verbose: {verbose}",
                ]
            )
        )
    xs = getxsatpathpts(
        path=t_path, numpts=numpoints, res=resdict[resolution], crs=crs, file=file
    )
    if file is None:
        print(xs.to_json())


if __name__ == "__main__":
    sys.exit(main(prog_name="nldi-xstool"))  # pragma: no cover
