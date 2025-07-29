"""Ancilarry."""
# import contextlib
from typing import Any
from typing import List
from typing import Tuple

import async_retriever as ar
import geopandas as gpd
import requests
from pygeohydro import NWIS
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon

from .ExtADCPBathy import ExtADCPBathy

# import numpy as np


def get_ext_bathy_xs(
    file: str, dist: float, lonstr: str, latstr: str, estr: str, acrs: str
) -> gpd.GeoDataFrame:
    """Extend a measured bathymetric cross-section to above water topography.

    Parameters
    ----------
    file : str
        Bathymetric survey file
    dist : float
        Distance to extend survey on both ends.
    lonstr : str
        String heading on longitude in file.
    latstr : str
        String heading on latitude in file.
    estr : str
        String heading on elevation in file.
    acrs : str
        String heading on crs code of measured lon/lat values, for example: espg:4326.

    Returns
    -------
    gpd.GeoDataFrame
        Geopandas dataframe of complete cross-section.
    """
    exs = ExtADCPBathy(
        file=file, dist=dist, lonstr=lonstr, latstr=latstr, estr=estr, acrs=acrs
    )

    return exs.get_xs_complete()


# The following function converts NGVD29 to NAVD88 if gage is in NGVD29 using
# NOAA NGS Vertcon service api
# https://www.ngs.noaa.gov/web_services/ncat/lat-long-height-service.shtml


def get_gage_datum(gagenum: str, verbose: bool = False) -> float:
    """Returns the datum of USGS gage in meters.

    Function uses the NOAA NGS Vertcon service to convert NGVD29 to NAVD88 if necessary.

    Parameters
    ----------
    gagenum : str
        USGS Gage number
    verbose : bool, optional
        Verbose output, by default False

    Returns
    -------
    float
        USGS Gage datum in meters
    """
    si = NWIS().get_info({"site": gagenum}, expanded=True)
    if si["alt_datum_cd"].values[0] != "NGVD29":
        # print('non-conversion')
        return float(si["alt_va"].values[0] * 0.3048)
    # print('conversion')
    url = "https://www.ngs.noaa.gov/api/ncat/llh"
    lat_str = "dec_lat_va"
    lon_str = "dec_long_va"

    alt_str = "alt_va"
    indatum_str = "coord_datum_cd"
    outdatum_str = "NAD83(2011)"
    in_vert_dataum_str = "NGVD29"
    out_vert_dataum_str = "NAVD88"
    if f"{si[indatum_str].values[0]}" == "NAD83":
        indatum = "NAD83(2011)"
    else:
        indatum = f"{si[indatum_str].values[0]}"

    ohgt = float(si[alt_str].values[0]) * 0.3048

    tmplonstr = si[lon_str].values[0]

    if len(str(tmplonstr)) == 6:
        tmplonstr = f"0{str(tmplonstr)}"

    payload = {
        "lat": f"{si[lat_str].values[0]}",
        "lon": f"{tmplonstr}",
        "orthoHt": repr(ohgt),
        "inDatum": indatum,
        "outDatum": outdatum_str,
        "inVertDatum": in_vert_dataum_str,
        "outVertDatum": out_vert_dataum_str,
    }
    resp = ar.retrieve_json([url], [{"params": payload}])[0]
    if verbose:
        print(f"{si[indatum_str].values[0]}")
        print(f"payload: {payload}")
        print(resp)
    return float(resp["destOrthoht"])


# Resolution types and their respective IDs for the Rest Service
res_types = {
    "res_1m": 18,
    "res_3m": 19,
    "res_5m": 20,
    "res_10m": 21,
    "res_30m": 22,
    "res_60m": 23,
}
# res_types = {'res_1m': 1, 'res_3m': 2, 'res_5m': 3, 'res_10m': 4, 'res_30m': 5, 'res_60m': 6}
dim_order = {"latlon": 0, "lonlat": 1}
# Create a bounding box from any geo type
# 'width' is in meters. It is the width of the buffer to place around the input geometry


def make_bbox(shape_type: str, coords: List[Tuple[float, float]], width: int) -> Any:
    """Return a bounding box of the coordinates buffered by width.

    Parameters
    ----------
    shape_type : str
        Shapetype one of: point, line, polygon
    coords : List[Tuple]
        List of coordinate tuples
    width : int
        Width in meters

    Returns
    -------
    Any
        Bounding box of geometry (minx, miny, maxx, maxy)
    """
    if shape_type == "point":
        shape = Point(coords)

    elif shape_type == "line":
        shape = LineString(coords)

    elif shape_type == "polygon":
        shape = Polygon(coords)

    converted_width = convert_width(width)
    buff_shape = shape.buffer(converted_width)
    return buff_shape.bounds


# Convert the width of the buffer from meters to 'degree'
# This is NOT a precise conversion, just a quick overestimation
# Maybe fix this later


def convert_width(width: int) -> int:
    """Buffer bbox geometry with specified width.

    This is an esitmation and is not precise.

    Parameters
    ----------
    width : int
        Width in meters to bffer geometries bounding box.

    Returns
    -------
    int
        buffer in degrees
    """
    factor = 1 / 70000
    dist = factor * width
    return int(dist)


# Get request from arcgis Rest Services


# @typeguard_ignore
def get_dem(bbox: Tuple[float, float, float, float], res_type: str) -> bool:
    """Esri map service query of 3DEPElevationIncex using bounding box.

    Return the True if res_type (Resolution of 3DEP elevation) intersects bounding box (bbox)

    Parameters
    ----------
    bbox : Tuple[float, float, float, float]
        (minx, miny, maxx, maxy)
    res_type : str
        Key in: res_types = {"res_1m": 18, "res_3m": 19,"res_5m": 20,
            "res_10m": 21,"res_30m": 22,"res_60m": 23,}

    Returns
    -------
    bool
        True if bbox intersects 3DEP elevation with res_type
    """
    minx = str(bbox[0])
    miny = str(bbox[1])
    maxx = str(bbox[2])
    maxy = str(bbox[3])
    res_id = res_types[res_type]
    return_val = False
    domain = "https://index.nationalmap.gov/"
    path = f"arcgis/rest/services/3DEPElevationIndex/MapServer/{res_id}/query"
    url = domain + path
    payload = {
        # "where": "",
        # "text": "",
        # "objectIds": "",
        # "time": "",
        "geometry": '{xmin:"'
        + minx
        + '",ymin:"'
        + miny
        + '",xmax:"'
        + maxx
        + '",ymax:"'
        + maxy
        + '",spatialReference:{wkid:4326}}',
        "geometryType": "esriGeometryEnvelope",
        "inSR": "EPSG:4326",
        "spatialRel": "esriSpatialRelIntersects",
        # "relationParam": "",
        # "outFields": "",
        "returnGeometry": "true",
        # "returnTrueCurves": "false",
        "maxAllowableOffset": "100",
        "geometryPrecision": "3",
        "outSR": "EPSG:4326",
        # "having": "",
        # "returnIdsOnly": "false",
        # "returnCountOnly": "false",
        # "orderByFields": "",
        # "groupByFieldsForStatistics": "",
        # "outStatistics": "",
        # "returnZ": "false",
        # "returnM": "false",
        # "gdbVersion": "",
        # "historicMoment": "",
        # "returnDistinctValues": "false",
        # "resultOffset": "",
        # "resultRecordCount": "",
        # "queryByDistance": "",
        # "returnExtentOnly": "false",
        # "datumTransformation": "",
        # "parameterValues": "",
        # "rangeValues": "",
        # "quantizationParameters": "",
        "featureEncoding": "esriDefault",
        "f": "geojson",
    }
    try:
        r = requests.get(url, params=payload, timeout=30)
        r.raise_for_status()
        resp = r.json()
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    # If the Rest Services has a 200 response
    if "features" in resp:
        # If the features are not empty, then the DEM exist
        if resp["features"] != []:
            return_val = True
        # If features are empty, then no DEM
        if resp["features"] == []:
            return_val = False
    # If 'error', then there was an unsuccessful request
    if "error" in resp:
        return_val = False
    return return_val


# The function to loop thru all resolutions and submit queries


def query_dems(
    shape_type: str, coords: List[Tuple[float, float]], width: int = 100
) -> Any:
    """Query 3DEPElevation.

     Index based on shape type and coordinates for available spatial resolution.

    Parameters
    ----------
    shape_type : str
        One of: point, line, polygon
    coords : List[Tuple[float, float]]
        List of coordinate tuples, for example: [(x,y), (x,y)].
    width : int, optional
        Width to buffer bounding box of shape, by default 100

    Returns
    -------
    Any
        Dictionary of query keys for example: res_1m, and bool intersection values.
    """
    bbox = make_bbox(shape_type, coords, width)  # Make the bbox
    # Loop thru all resolutions and submit a query for each one
    return query_dems_bbox(bbox)


def query_dems_bbox(bbox: Tuple[float, float, float, float]) -> Any:
    """Query 3DEP Elevation Index for available spatial resolution.

    Uses esriSpatialRelIntersects - Query Geometry Intersects Target Geometry.

    Parameters
    ----------
    bbox : Tuple[float]
        (minx, miny, maxx, maxy)

    Returns
    -------
    Dict
        Boolian values associated with resolution keys.
    """
    return {res_type: get_dem(bbox, res_type) for res_type in res_types}
