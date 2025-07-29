"""Tools for extending USGS measured Bathymetry (preliminary)."""
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from geopandas.array import points_from_xy
from shapely.geometry import Point

from nldi_xstool.nldi_xstool import getxsatendpts


class ExtADCPBathy:
    """Class to facilitate extending USGS measured bathymetry cross-sections."""

    def __init__(
        self, file: str, dist: float, lonstr: str, latstr: str, estr: str, acrs: str
    ) -> None:
        """Initializes an ExtADCPBathy instance.

        Args:
            file: str - The file path to read data from.
            dist: float - The distance value.
            lonstr: str - The longitude string.
            latstr: str - The latitude string.
            estr: str - The elevation string.
            acrs: str - The coordinate reference system.

        Raises:
            FileNotFoundError: If the specified file does not exist.

        """
        self.afile = Path(file)
        if not self.afile.exists():
            raise FileNotFoundError("File does not exist")  # Ensure the file exists
        self.adata = pd.read_csv(self.afile)

        # Create a GeoDataFrame from the CSV data
        self.agdf = gpd.GeoDataFrame(
            self.adata, geometry=points_from_xy(self.adata[lonstr], self.adata[latstr])
        ).set_crs(acrs)

        self.agdf["elevation"] = self.adata[estr]

        # Convert CRS to Albers Conic for geometry calculations
        self.agdf = self.agdf.to_crs("epsg:5071")

        # Clean up dataframe by deleting original coordinate and elevation columns
        self.agdf.drop(columns=[lonstr, latstr, estr], inplace=True)

        self.ext = dist
        self.crs = acrs
        self.xs_complete = gpd.GeoDataFrame()

        self._build_geom()

    @staticmethod
    def _distance(p1: Point, p2: Point) -> float:
        """Calculate the Euclidean distance between two points.

        Args:
            p1: First point.
            p2: Second point.

        Returns:
            Distance between p1 and p2.
        """
        return np.linalg.norm(np.array(p2) - np.array(p1))

    def _build_geom(self) -> None:
        """Builds and extends the geometry based on the input data."""
        npts = len(self.agdf)
        p1 = np.array(self.agdf.geometry.iloc[0].coords[0])
        p2 = np.array(self.agdf.geometry.iloc[npts - 1].coords[0])

        # Calculate the angle and distance for extending points
        dx, dy = p2 - p1
        theta = np.arctan2(dy, dx)
        length = np.linalg.norm(p2 - p1)

        # Calculate new points for extending the line
        p1_new = p1 - (self.ext + 1) * np.array([np.cos(theta), np.sin(theta)])
        p2_new = p1 + (length + self.ext + 1) * np.array([np.cos(theta), np.sin(theta)])

        # Create dataframes for new points
        df_pre = pd.DataFrame({"lon": [p1_new[0], p1[0]], "lat": [p1_new[1], p1[1]]})
        df_post = pd.DataFrame({"lon": [p2[0], p2_new[0]], "lat": [p2[1], p2_new[1]]})

        # Create GeoDataFrames for the new points and convert to original CRS
        gdf_pre = gpd.GeoDataFrame(
            df_pre, geometry=gpd.points_from_xy(df_pre.lon, df_pre.lat)
        ).set_crs("epsg:5071")
        gdf_post = gpd.GeoDataFrame(
            df_post, geometry=gpd.points_from_xy(df_post.lon, df_post.lat)
        ).set_crs("epsg:5071")

        new_df_pre = self._get_xs(gdf_pre.to_crs("epsg:4326"), int(self.ext), 1).to_crs(
            "epsg:5071"
        )
        new_df_post = self._get_xs(
            gdf_post.to_crs("epsg:4326"), int(self.ext), 1
        ).to_crs("epsg:5071")

        # Prepare final GeoDataFrame
        for df in [new_df_pre, new_df_post]:
            df.drop(columns=["distance"], inplace=True)
            df["code"] = "0"

        self.agdf["code"] = "1"
        self.xs_complete = gpd.GeoDataFrame(
            pd.concat([new_df_pre, self.agdf, new_df_post], ignore_index=True),
            crs="epsg:5071",
        )

        # Calculate station values
        p1_coords = np.array(self.xs_complete.geometry.iloc[0].coords[0])
        self.xs_complete["station"] = self.xs_complete.geometry.apply(
            lambda geom: self._distance(p1_coords, np.array(geom.coords[0]))
        )

    def _get_xs(
        self, gdf: gpd.GeoDataFrame, numpts: int, res: float
    ) -> gpd.GeoDataFrame:
        """Wrapper for nldi-xstool.getxsatendpts to get cross-sections at endpoints.

        Args:
            gdf: GeoDataFrame with endpoint geometries.
            numpts: Number of points.
            res: Resolution.

        Returns:
            GeoDataFrame with cross-sections.
        """
        return getxsatendpts(
            [
                (gdf.geometry[0].x, gdf.geometry[0].y),
                (gdf.geometry[1].x, gdf.geometry[1].y),
            ],
            numpts=numpts,
            crs="epsg:4326",
            res=res,
        )

    def get_xs_complete(self) -> gpd.GeoDataFrame:
        """Return extended cross-section.

        Returns:
            GeoDataFrame with extended cross-section and spatial reference information.
        """
        xs_complete_crs = self.xs_complete.to_crs(self.crs)
        xs_complete_crs["spatial_ref"] = self.crs
        return xs_complete_crs
