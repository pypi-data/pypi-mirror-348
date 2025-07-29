"""Centerline."""
from typing import Any
from typing import Tuple

import geopandas as gpd
import numpy as np
import numpy.typing as npt

from .tspline import curvature
from .tspline import tspline


class Centerline:
    """Centerline.

    class to take a centerline as a shapefile and create a tension spline to be used
    with inherited class curvilinear grid
    """

    def __init__(
        self: "Centerline", center_shp: gpd.GeoDataFrame, nx: int, tension: float
    ) -> None:
        """Init Centerline class.

        Args:
            center_shp (gpd.GeoDataFrame): centerline shape
            nx (int): Number of interpolatin points.
            tension (float): Centerline tension-spline interpolation tension (.1 - 100.)
        """
        self.center_shp = center_shp
        self.gpdata = center_shp.geometry
        self.x = np.empty(0, dtype=np.double)
        self.y = np.empty(0, dtype=np.double)
        self.tension = tension
        self.numclpts = 0
        self.numInterpPts = nx
        self.si = np.empty(0, dtype=np.double)
        self.temp = np.empty(0, dtype=np.double)
        self.yp = np.empty(0, dtype=np.double)
        self.xo_interp = np.empty(0, dtype=np.double)
        self.yo_interp = np.empty(0, dtype=np.double)
        self.phi_interp = np.empty(0, dtype=np.double)
        self.r_interp = np.empty(0, dtype=np.double)
        self.stot = np.empty(0, dtype=np.double)
        self.sout = np.empty(0, dtype=np.double)
        self.__initialize()
        self.__getspline(nx, self.tension)

    def __initialize(self: "Centerline") -> None:
        tx, ty = zip(*(g.xy for g in self.gpdata))
        self.x = np.array(tx, dtype=np.double).squeeze()
        self.y = np.array(ty, dtype=np.double).squeeze()
        self.numclpts = self.x.size
        print(self.numclpts)

    # def description(self):
    #     return "{} used the shapfile {}".format("centerline", self.center_shp)

    # def getCLShapeFile(self):
    #     return self.center_shp

    # def getlength(self): #
    #     return

    def getpoints(
        self: "Centerline",
    ) -> Tuple[npt.NDArray[Any], npt.NDArray[Any]]:
        """Get centerline points.

        Returns:
            [type]: [description]
        """
        return self.x, self.y

    def getinterppts(self) -> Tuple[npt.NDArray[Any], npt.NDArray[Any]]:
        """Get interpolated centerline points."""
        return self.xo_interp, self.yo_interp

    def getinterppts_dyn(
        self: "Centerline", numinterppts: int, tension: float
    ) -> Tuple[npt.NDArray[Any], npt.NDArray[Any]]:
        """Get interpolated centerline points when user moving points interactively.

        Args:
            numinterppts (int): [description]
            tension (float): [description]

        Returns:
            [type]: [description]
        """
        print(tension)
        self.__getspline(numinterppts, tension)
        return self.xo_interp, self.yo_interp

    def getphiinterp(self: "Centerline", index: int) -> Any:  # noqa D102
        return self.phi_interp[index]

    def __getspline(self: "Centerline", numinterppts: int, tension: float) -> None:
        self.numInterpPts = numinterppts
        self.tension = tension
        self.xo_interp = np.zeros(self.numInterpPts, dtype=np.double)
        self.yo_interp = np.zeros(self.numInterpPts, dtype=np.double)
        self.phi_interp = np.zeros(self.numInterpPts, dtype=np.double)
        self.r_interp = np.zeros(self.numInterpPts, dtype=np.double)
        self.sout = np.zeros(self.numInterpPts, dtype=np.double)

        pts = gpd.GeoSeries(gpd.points_from_xy(self.x, self.y, crs=self.gpdata.crs))
        self.si = pts.distance(pts.shift(1)).fillna(0.0).cumsum().to_numpy(np.double)
        self.temp = np.zeros(self.numclpts, dtype=np.double)
        self.yp = np.zeros(self.numclpts, dtype=np.double)

        self.stot = self.si[-1]
        self.sout = np.arange(self.numInterpPts) * self.stot / (self.numInterpPts - 1)

        if self.numclpts < 3:
            self.yp = np.zeros(3, dtype=np.double)
            self.temp = np.zeros(3, dtype=np.double)
            sitmp = np.array(
                [self.si[0], self.si[1] * 0.5, self.si[1]], dtype=np.double
            )

            txctmp = np.array(
                [
                    self.x[0],
                    self.x[0] + (self.x[1] - self.x[0]) * 0.5,
                    self.x[1],
                ],
                dtype=np.double,
            )

            tyctmp = np.array(
                [
                    self.y[0],
                    self.y[0] + (self.y[1] - self.y[0]) * 0.5,
                    self.y[1],
                ],
                dtype=np.double,
            )

            tspline(
                sitmp,
                txctmp,
                3,
                self.sout,
                self.xo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
            tspline(
                sitmp,
                tyctmp,
                3,
                self.sout,
                self.yo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
        else:
            tspline(
                self.si,
                self.x,
                self.numclpts,
                self.sout,
                self.xo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
            tspline(
                self.si,
                self.y,
                self.numclpts,
                self.sout,
                self.yo_interp,
                self.numInterpPts,
                self.tension,
                self.yp,
                self.temp,
            )
        self.__calc_curvature()

    def __calc_curvature(self: "Centerline") -> None:
        """Calculate curvature."""
        self.phi_interp, self.r_interp = curvature(
            self.xo_interp, self.yo_interp, self.stot
        )
