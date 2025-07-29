"""pygeoapi implementation of getxsatendpts."""
import logging
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from geopandas import GeoDataFrame
from pygeoapi.process.base import BaseProcessor

from nldi_xstool.nldi_xstool import getxsatpathpts

# from typing import Any
# from typing import Tuple


LOGGER = logging.getLogger(__name__)

PROCESS_METADATA = {
    "version": "0.1.0",
    "id": "nldi-xsatendpts",
    "title": "NLDI xsatendpts process",
    "description": "NLDI xsatendpts process",
    "jobControlOptions": ["sync-execute"],
    "keywords": ["NLDI xsatendpts"],
    "links": [
        {
            "type": "text/html",
            "rel": "canonical",
            "title": "information",
            "href": "https://example.org/process",
            "hreflang": "en-US",
        }
    ],
    "inputs": [
        {
            "id": "path",
            "title": "path",
            "input": {
                "literalDataDomain": {
                    "dataType": "list",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        {
            "id": "numpts",
            "title": "numpts",
            "input": {
                "literalDataDomain": {
                    "dataType": "int",
                    "valueDefinition": {"anyValue": True},
                }
            },
            "minOccurs": 1,
            "maxOccurs": 1,
        },
        {
            "id": "3dep_res",
            "title": "resolution",
            "abstract": "Resolution of 3dep elevation data",
            "minOccurs": 1,
            "maxOccurs": 1,
            "input": {
                "literalDataDomain": {
                    "dataType": "enum",
                    "valueDefinition": {
                        "anyValue": False,
                        "defaultValue": "10",
                        "possibleValues": ["30", "10", "5", "3", "1"],
                    },
                }
            },
        },
    ],
    "outputs": [
        {
            "id": "nldi-xsatpathpts-response",
            "title": "output nldi-xsatpathpts",
            "output": {"formats": [{"mimeType": "application/json"}]},
        }
    ],
    "example": {
        "inputs": [
            {
                "id": "path",
                "value": [
                    (-108.45263, 38.97755),
                    (-108.45350, 38.97800),
                    (-108.454393, 38.977915),
                    (-108.45495, 38.97837),
                ],
                "type": "text/plain",
            },
            {"id": "numpts", "value": "101", "type": "text/plain"},
            {"id": "3dep_res", "value": "1", "type": "text/plain"},
        ]
    },
}


class NLDIxsatpathptsProcessor(BaseProcessor):  # type: ignore
    """NLDI xsatpathpoints Processor."""

    def __init__(self, provider_def: Dict[str, Any]) -> None:
        """Initialize object.

        :param provider_def: provider definition
        :returns: pygeoapi.process.NLDIDelineateProcessor
        """
        BaseProcessor.__init__(self, provider_def, PROCESS_METADATA)

    def execute(self, data: List[Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
        """Execute processor."""
        print("before data assign")
        print(data)
        # reformat data into dict with just needed values
        newdata = {d["id"]: d["value"] for d in data}
        mimetype = "application/json"
        fpath = newdata["path"]
        numpts = int(newdata["numpts"])
        res = int(newdata["3dep_res"])

        print(fpath, numpts, res)

        timebefore = time.perf_counter()

        print("before function")
        results = GeoDataFrame(
            getxsatpathpts(
                path=fpath,
                numpts=numpts,
                res=res,
                crs="epsg:4326",
            )
        )
        print("after function")
        # print(results)

        timeafter = time.perf_counter()
        totaltime = timeafter - timebefore
        print("Total Time:", totaltime)

        # outputs = [
        #     {"id": "nldi-xsatendpts-response", "value": results.__geo_interface__}
        # ]
        # print(results)
        return mimetype, results.__geo_interface__

    def __repr__(self) -> str:
        """Get representation."""
        return "<NLDIxsatendptsProcessor> {}".format("get xsatendpts")
