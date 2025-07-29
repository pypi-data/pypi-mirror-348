"""Main module."""
import sys
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import geopandas as gpd
import pandas as pd
import py3dep
from pynhd import NLDI
from shapely.geometry import LineString
from shapely.geometry import Point

from .PathGen import PathGen
from .XSGen import XSGen

# import numpy as np
# import xarray as xr

CRS = "epsg:3857"
ALT_CRS = "epsg:4326"


def dataframe_to_geodataframe(df: pd.DataFrame, crs: str) -> gpd.GeoDataFrame:
    """Convert pandas Dataframe to Geodataframe."""
    geometry = [Point(xy) for xy in zip(df.x, df.y)]
    df = df.drop(["x", "y"], axis=1)
    return gpd.GeoDataFrame(df, geometry=geometry, crs=crs)


def getxsatpathpts(
    path: List[Tuple[float, float]],
    numpts: int,
    crs: Optional[str] = ALT_CRS,
    file: Optional[str] = None,
    res: float = 10,
) -> gpd.GeoDataFrame:
    """Get elevation cross-section at user-defined path.

    Note 1:
        Cross-section is interpolated using 3DEP elevation services which does not
        include bathymetric data.

    Note 2:
        The parameter res specifices the spatial resolution of the 3DEP data that is
        interpolated to return elevation values of the cross-section points.  It does
        not specify the native spatial resolution of the 3DEP data.  If using this as a
        package the query_dems function in nldi-xstool.ancillary can be used to discover
        the available native resolution of the 3DEP data at the bounding box of the
        cross-section.

    Args:
        path (List[Tuple[float, float]]): List of tuples containing coordinate pairs
            of the path, for example: [(x1,y1), (x2,y2), (x3, y3)]
        numpts (int): Number of points to interpolate along path.
        crs (Optional[str], optional): crs of input data. Defaults to ALT_CRS.
        file (Optional[str], optional): path/to/file.json. Path to write json file.
            Defaults to None and returns a GeoDataFrame.
        res (float): Spatial resolution of 3DEP Dem data. Defaults to
            10 which is available throughout CONUS.

    Returns:
        gpd.GeoDataFrame: cross-section in a GeoDataFrame.
    """
    # print(path, type(path))
    lnst = [Point(pt[0], pt[1]) for pt in path]
    # print(ls1)
    d = {"name": ["xspath"], "geometry": [LineString(lnst)]}
    gpd_pth = gpd.GeoDataFrame(d, crs=crs).to_crs(CRS)
    # print(gpd_pth)
    # print(gpd_pth)
    xs = PathGen(path_geom=gpd_pth, ny=numpts)
    xs_line = xs.get_xs()
    # print(xs_line.head())
    # print(xs_line.total_bounds, xs_line.bounds)
    bb = xs_line.total_bounds - ((100.0, 100.0, -100.0, -100.0))
    # print('before dem', bb)
    dem = py3dep.get_map("DEM", tuple(bb), resolution=res, geo_crs=CRS, crs=CRS)
    # print('after dem')
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=("z", x), y=("z", y))
    pdsi = dsi.to_dataframe()
    gpdsi = dataframe_to_geodataframe(pdsi, crs=CRS)
    gpdsi["distance"] = _get_dist_path(gpdsi)
    gpdsi = gpdsi.to_crs(ALT_CRS)
    if file is not None:
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        with open(Path(file), "w") as f:
            f.write(gpdsi.to_json())
    return gpdsi


def getxsatendpts(
    path: List[Tuple[float, float]],
    numpts: int,
    crs: Optional[str] = ALT_CRS,
    file: Optional[str] = None,
    res: float = 10,
) -> gpd.GeoDataFrame:
    """Get cross-section at user defined endpoints.

    Note 1:
        Cross-section is interpolated using 3DEP elevation services which does not
        include bathymetric data.

    Note 2:
        The parameter res specifices the spatial resolution of the 3DEP data that is
        interpolated to return elevation values of the cross-section points.  It does
        not specify the native spatial resolution of the 3DEP data.  If using this as a
        package the query_dems function in nldi-xstool.ancillary can be used to discover
        the available native resolution of the 3DEP data at the bounding box of the
        cross-section.

    Args:
        path (List[Tuple[float, float]]): List of tuples containing coordinate pairs
            of the end-points in order from river-left to river-right,
            for example: [(x1,y1), (x2,y2)]
        numpts (int): Number of points to interpolate along path.
        crs (Optional[str], optional): crs of input data. Defaults to ``EPSG:4326``.
        file (Optional[str], optional): path/to/file.json. Path to write json file.
            Defaults to None and returns a GeoDataFrame.
        res (float): Spatial resolution of 3DEP Dem data. Defaults to
            10 which is available throughout CONUS.

    Returns:
        gpd.GeoDataFrame: cross-section in a GeoDataFrame.
    """
    lnst = [Point(pt[0], pt[1]) for pt in path]
    # print(lnst)
    d = {"name": ["xspath"], "geometry": [LineString(lnst)]}
    gpd_pth = gpd.GeoDataFrame(d, crs=crs).to_crs(CRS)
    # print(gpd_pth)
    # gpd_pth.set_crs(epsg=4326, inplace=True)
    # gpd_pth.to_crs(epsg=3857, inplace=True)
    # print(gpd_pth)
    xs = PathGen(path_geom=gpd_pth, ny=numpts)
    xs_line = xs.get_xs()
    # print(xs_line.head())
    # print(xs_line.total_bounds, xs_line.bounds)
    bb = xs_line.total_bounds - ((100.0, 100.0, -100.0, -100.0))
    # print("before dem", bb)
    dem = py3dep.get_map("DEM", tuple(bb), resolution=res, geo_crs=CRS, crs=CRS)

    # print("after dem")
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=("z", x), y=("z", y))
    pdsi = dsi.to_dataframe()

    gpdsi = dataframe_to_geodataframe(pdsi, crs=CRS)
    gpdsi["distance"] = _get_dist(gpdsi)
    gpdsi = gpdsi.to_crs(ALT_CRS)
    if file is not None:
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        with open(Path(file), "w") as f:
            f.write(gpdsi.to_json())
    return gpdsi


def _get_dist(gdf: gpd.GeoDataFrame) -> pd.Series:
    data = gdf.to_crs(epsg=5071)
    return data.distance(data.geometry[0])


def _get_dist_path(gdf: gpd.GeoDataFrame) -> pd.Series:
    data = gdf.to_crs(epsg=5071)
    return data.distance(data.shift(1).geometry).fillna(0)


def getxsatpoint(
    point: Tuple[float, float],
    numpoints: int,
    width: float,
    file: str = None,
    res: float = 10,
) -> gpd.GeoDataFrame:
    """Get cross-section at nearest stream-segment and closest intersecton to point.

    Function uses the U.S. Geological Survey's NLDI to find the nearest NHD stream-
    segment, and generate a cross-section perpendicular to the nearest intersection
    of the point and stream-segment.

    Note 1:
        Cross-section is interpolated using 3DEP elevation services which does not
        include bathymetric data.

     Note 2:
        The parameter res specifices the spatial resolution of the 3DEP data that is
        interpolated to return elevation values of the cross-section points.  It does
        not specify the native spatial resolution of the 3DEP data.  If using this as a
        package the query_dems function in nldi-xstool.ancillary can be used to discover
        the available native resolution of the 3DEP data at the bounding box of the
        cross-section.

    Args:
        point (Tuple[float, float]): _description_
        numpoints (int): _description_
        width (float): _description_
        file (str): _description_. Defaults to "".
        res (float): _description_. Defaults to 10.

    Returns:
        gpd.GeoDataFrame: _description_
    """
    df = pd.DataFrame(
        {"pointofinterest": ["this"], "Lat": [point[1]], "Lon": [point[0]]}
    )
    gpd_pt = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Lon, df.Lat), crs=ALT_CRS
    )
    gpd_pt = gpd_pt.to_crs(CRS)
    nldi = NLDI()
    try:
        _comid = nldi.comid_byloc(tuple(point))  # type: ignore
    except Exception as ex:  # pragma: no cover
        # print(f'Error: {ex} unable to find comid - check lon lat coords')
        sys.exit(f"Error: {ex} unable to find comid - check lon lat coords")

    if isinstance(_comid, gpd.GeoDataFrame):
        comid = _comid.comid.values[0]
    else:
        comid = _comid[0].comid.values[0]
    # print(f'comid = {comid}')
    _strm_seg = nldi.getfeature_byid("comid", comid)
    if isinstance(_strm_seg, gpd.GeoDataFrame):
        strm_seg = _strm_seg.to_crs(CRS)
    else:
        strm_seg = _strm_seg[0].to_crs(CRS)
    xs = XSGen(point=gpd_pt, cl_geom=strm_seg, ny=numpoints, width=width, tension=10.0)
    xs_line = xs.get_xs()
    # print(comid, xs_line)
    # get topo polygon with buffer to ensure there is enough topography to interpolate
    # xs line with coarsest DEM (30m) 100. m should
    bb = xs_line.total_bounds - ((100.0, 100.0, -100.0, -100.0))
    dem = py3dep.get_map("DEM", tuple(bb), resolution=res, geo_crs=CRS, crs=CRS)
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=("z", x), y=("z", y))
    pdsi = dsi.to_dataframe()
    gpdsi = dataframe_to_geodataframe(pdsi, crs=CRS)
    gpdsi["distance"] = _get_dist(gpdsi)
    gpdsi = gpdsi.to_crs(ALT_CRS)
    if file is not None:
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        with open(Path(file), "w") as f:
            f.write(gpdsi.to_json())
    return gpdsi
