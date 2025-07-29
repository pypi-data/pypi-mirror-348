"""Function to interpolate a tensioned spline based on user defined x,y points.

Code based on Fortran code developed by Jonathan Nelson (jmn@usgs.gov) at USGS.
"""
from typing import Any
from typing import Tuple

import numpy as np
import numpy.typing as npt
from numba import prange

# from numba import njit

# from typeguard import typeguard_ignore

# @typeguard_ignore
# @njit(
#     "(f8[::1], f8[::1], i8, f8[::1], f8[::1], i8, f8, f8[::1], f8[::1])",
#     cache=True,
# )  # type: ignore


def tspline(
    x: npt.NDArray[Any],
    y: npt.NDArray[Any],
    n: int,
    xout: npt.NDArray[Any],
    yout: npt.NDArray[Any],
    iout: int,
    sigma: float,
    yp: npt.NDArray[Any],
    temp: npt.NDArray[Any],
) -> None:
    """Tension spline generator.

    Parameters
    ----------
    x : npt.NDArray[Any]
        [description]
    y : npt.NDArray[Any]
        [description]
    n : int
        [description]
    xout : npt.NDArray[Any]
        [description]
    yout : npt.NDArray[Any]
        [description]
    iout : int
        [description]
    sigma : float
        [description]
    yp : npt.NDArray[Any]
        [description]
    temp : npt.NDArray[Any]
        [description]
    """
    nm1 = n - 2
    delx1 = x[1] - x[0]
    dx1 = (y[1] - y[0]) / delx1
    delx2 = x[2] - x[1]
    delx12 = x[2] - x[0]
    c1 = -(delx12 + delx1) / delx12 / delx1
    c2 = delx12 / delx1 / delx2
    c3 = -delx1 / delx12 / delx2
    slpp1 = c1 * y[0] + c2 * y[1] + c3 * y[2]
    deln = x[n - 1] - x[nm1]
    delnm1 = x[nm1] - x[n - 3]
    delnn = x[n - 1] - x[n - 3]
    c1 = (delnn + deln) / delnn / deln
    c2 = -delnn / deln / delnm1
    c3 = deln / delnn / delnm1
    slppn = c3 * y[n - 3] + c2 * y[nm1] + c1 * y[n - 1]
    sigmap = np.fabs(sigma) * (float(n - 2)) / (x[n - 1] - x[0])
    dels = sigmap * delx1
    exps = np.exp(dels)
    sinhs = 0.5 * (exps - 1.0 / exps)
    sinhin = 1.0 / (delx1 * sinhs)
    diag1 = sinhin * (dels * 0.5 * (exps + 1.0 / exps) - sinhs)
    diagin = 1.0 / diag1
    yp[0] = diagin * (dx1 - slpp1)
    spdiag = sinhin * (sinhs - dels)
    temp[0] = diagin * spdiag
    dx2 = 0
    for i in range(nm1 + 1):
        delx2 = x[i + 1] - x[i]
        dx2 = (y[i + 1] - y[i]) / delx2
        dels = sigmap * delx2
        exps = np.exp(dels)
        sinhs = 0.5 * (exps - 1.0 / exps)
        sinhin = 1.0 / (delx2 * sinhs)
        diag2 = sinhin * (dels * (0.5 * (exps + 1.0 / exps)) - sinhs)
        diagin = 1.0 / (diag1 + diag2 - spdiag * temp[i - 1])
        yp[i] = diagin * (dx2 - dx1 - spdiag * yp[i - 1])
        spdiag = sinhin * (sinhs - dels)
        temp[i] = diagin * spdiag
        dx1 = dx2
        diag1 = diag2
    diagin = 1.0 / (diag1 - spdiag * temp[nm1])
    yp[n - 1] = diagin * (slppn - dx2 - spdiag * yp[nm1])
    np1 = n
    for i in range(1, np1):
        ibak = np1 - i - 1
        yp[ibak] = yp[ibak] - temp[ibak] * yp[ibak + 1]
    a = x[0]
    b = x[1]
    nj = 1
    for i in range(iout):
        if xout[i] > b:
            while xout[i] > b:
                a = b
                nj = nj + 1
                b = x[nj]

        del1 = xout[i] - a
        del2 = b - xout[i]
        dels = b - a
        exps1 = np.exp(sigmap * del1)
        sinhd1 = 0.5 * (exps1 - 1.0 / exps1)
        exps = np.exp(sigmap * del2)
        sinhd2 = 0.5 * (exps - 1.0 / exps)
        exps = exps * exps1
        sinhs = 0.5 * (exps - 1.0 / exps)
        yout[i] = (yp[nj] * sinhd1 + yp[nj - 1] * sinhd2) / sinhs + (
            (y[nj] - yp[nj]) * del1 + (y[nj - 1] - yp[nj - 1]) * del2
        ) / dels


# @njit("UniTuple(f8[::1], 2)(f8[::1], f8[::1], f8)", cache=True)  # type: ignore
def curvature(
    xs: npt.NDArray[Any], ys: npt.NDArray[Any], stot: npt.NDArray[np.float64]
) -> Tuple[npt.NDArray[Any], npt.NDArray[Any]]:
    """Compute curvature of a spline.

    Parameters
    ----------
    xs : npt.NDArray[Any]
        [description]
    ys : npt.NDArray[Any]
        [description]
    stot : float
        [description]
    """
    npts = xs.size
    phi_interp = np.zeros(npts, dtype="f8")
    r_interp = np.zeros(npts, dtype="f8")
    for i in prange(1, npts):
        dx = xs[i] - xs[i - 1]
        dy = ys[i] - ys[i - 1]
        if dx == 0.0:
            if dy > 0.0:
                phi_interp[i] = np.pi / 2.0
            elif dy < 0.0:
                phi_interp[i] = -1.0 * np.pi / 2.0
        else:
            phi_interp[i] = np.arctan2(dy, dx)
    phi_interp[0] = (2.0 * phi_interp[1]) - phi_interp[2]
    scals = stot / (npts - 1)
    for i in prange(1, npts):
        dx = xs[i] - xs[i - 1]
        dphi = np.fabs(phi_interp[i]) - np.fabs(phi_interp[i - 1])
        if dphi <= 0.0001:
            r_interp[i] = 100000000.0
        else:
            r_interp[i] = scals / dphi
    return phi_interp, r_interp
