#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

# This code adapted from:
# https://github.com/geopython/OWSLib/blob/master/examples/wms-getfeatureinfo.py

import copy
from owslib.wfs import WebFeatureService
import logging
import lxml.etree as etree
from lxml.builder import ElementMaker
from pydov.util import location
from osgeo import ogr, osr
import json

log = logging.getLogger(__name__)

HELSINKI_GEOSERVER_OPENDATA_URL = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs"
HELSINKI_GEOSERVER_INTERNAL_URL = "https://kartta.hel.fi/ws/geoserver/helsinki/wfs"


class GeoServer_Reader_json:
    wfs = None
    geo_url = None
    layername = None
    schema = None
    use_auth = None
    username = None
    password = None

    GML_ID = "gml_id"
    GML_GEOM = "geom"

    def __init__(self, username=None, password=None):
        if not GeoServer_Reader_json.username or username:
            # Conditional setting of creds
            GeoServer_Reader_json.set_auth_credentials(username, password)

    @staticmethod
    def set_logging_level(level=logging.DEBUG):
        owslib_log = logging.getLogger("owslib")
        owslib_log.setLevel(level)

    @staticmethod
    def set_auth_credentials(username, password):
        GeoServer_Reader_json.username = username
        GeoServer_Reader_json.password = password

    def _init_wfs(self):
        url_to_use = None
        if self.use_auth:
            url_to_use = HELSINKI_GEOSERVER_INTERNAL_URL
        else:
            url_to_use = HELSINKI_GEOSERVER_OPENDATA_URL

        if self.geo_url:
            if url_to_use != self.geo_url:
                self.wfs = None
        if self.wfs:
            return

        self.geo_url = url_to_use
        version = "2.0.0"
        wfs = WebFeatureService(
            self.geo_url,
            version=version,
            username=self.username,
            password=self.password,
        )

        self.wfs = wfs

        return wfs

    def get_schema(self):
        self._init_wfs()
        layer_schema = self.wfs.get_schema(self.layername)

        return layer_schema

    def query(
        self, fields, filter={}, return_single_result=True, limit_results_to=1000
    ):
        self._init_wfs()

        if not isinstance(fields, list):
            raise ValueError("Need a list of fields to harvest from response!")
        if len(fields) == 0:
            raise ValueError("Field list is empty!")
        if not filter:
            raise ValueError("Need filter for query()!")
        if isinstance(filter, location.GmlObject):
            filter_fes = self._filter_polygon(filter)
        else:
            filter_fes = self._filter_key_value(filter)
        log.debug("Filter: %s" % filter_fes)

        log.debug("Get feature from: %s" % self.layername)
        response = self.wfs.getfeature(
            typename=self.layername,
            # srsname='urn:ogc:def:crs:EPSG::4326',
            # srsname='EPSG:3879',
            filter=filter_fes,
            startindex=0,
            method="post",
            outputFormat="json",
        )

        raw = json.loads(response.read())
        # log.info(raw)
        returned = raw.get("numberReturned")
        if limit_results_to and returned > limit_results_to:
            log.error("Argh! Too much data.")
            raise ValueError(
                "Too much data. Faulty filter! Expecting less than %d, but got %d."
                % (limit_results_to, returned)
            )
        kdata_out = []
        kdata = None
        for feature in raw.get("features"):
            kdata = feature.get("properties")
            kdata["id"] = feature.get("id")
            kdata["srs"] = raw.get("crs", {}).get("properties", {}).get("name")
            kdata["geom"] = [
                {
                    "type": "Feature",
                    "geometry": feature.get("geometry"),
                    "properties": {
                        "id": feature.get("id"),
                    },
                }
            ]
            if return_single_result:
                break
            kdata_out.append(kdata)

        if return_single_result:
            return returned, kdata

        return returned, kdata_out

    @staticmethod
    def _filter_key_value(filter_dict):
        # Was: def _filter(**kwargs):
        # name = list(kwargs.keys())[0]
        # value = kwargs[name]
        keys = list(filter_dict.keys())
        if not keys or len(keys) > 1:
            raise ValueError("Invalid filter!")
        name = keys[0]
        value = filter_dict[name]
        if not isinstance(value, str):
            raise ValueError("Filter value needs to be a string!")

        E = ElementMaker(namespace="http://www.opengis.net/fes/2.0")
        et = E.root(
            E.Filter(E.PropertyIsEqualTo(E.ValueReference(name), E.Literal(value)))
        )
        filter_fes = etree.tostring(
            et, encoding="ascii", method="xml", xml_declaration=False
        ).decode("ascii")

        """
        <fes:Filter
            xmlns:fes="http://www.opengis.net/fes/2.0">
            <fes:PropertyIsEqualTo>
                <fes:ValueReference>kiinteistotunnus</fes:ValueReference>
                <fes:Literal>09100501240007</fes:Literal>
            </fes:PropertyIsEqualTo>
        </fes:Filter>
        """

        return filter_fes

    def _filter_polygon(self, filter_polygon):
        if not isinstance(filter_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        E = ElementMaker(namespace="http://www.opengis.net/fes/2.0")
        et = E.root(
            E.Filter(
                E.Intersects(
                    E.ValueReference(self.schema["geometry_column"]),
                    filter_polygon.get_element(),
                )
            )
        )
        filter_fes = etree.tostring(
            et, encoding="ascii", method="xml", xml_declaration=False
        ).decode("ascii")

        return filter_fes

    def _schema_to_fieldlist(self):
        if not self.schema:
            raise ValueError("Schema is missing!")
        if not isinstance(self.schema, dict):
            raise ValueError("Schema is not a dict!")
        if "properties" not in self.schema:
            raise ValueError("Invalid schema definition!")
        fields = list(self.schema["properties"].keys())

        return fields

    def _json_to_gml(self, data):
        if not data["geom"][0]["geometry"]:
            raise ValueError("Gometry missing!")

        # log.info(data)
        dump = json.dumps(data["geom"][0]["geometry"])
        geom = ogr.CreateGeometryFromJson(dump)
        spatialReference = osr.SpatialReference()
        # spatialReference.SetWellKnownGeogCS(data['srs'])
        spatialReference.ImportFromEPSG(3879)
        spatialReference.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        geom.AssignSpatialReference(spatialReference)  # 'urn:ogc:def:crs:EPSG::3879'
        gml = geom.ExportToGML(
            options=[
                "SRSDIMENSION_LOC=GEOMETRY",
                "FORMAT=GML32",
                "GML3_LONGSRS=YES",
                "GMLID=%s" % data["id"],
                "NAMESPACE_DECL=YES",
            ]
        )
        # log.info(gml)
        return location.GmlObject(gml)

    def convert_data(self, data):
        return self._json_to_gml(data)

    def get_geometry(self, data):
        # create a geometry from coordinates
        new_geom = copy.deepcopy(data["geom"])
        dump = json.dumps(new_geom[0]["geometry"])
        geom = ogr.CreateGeometryFromJson(dump)

        # create coordinate transformation
        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(3879)
        inSpatialRef.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(4326)
        # outSpatialRef.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

        coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

        # transform
        geom.Transform(coordTransform)

        new_geom[0]["geometry"] = geom.ExportToJson()
        return json.dumps(new_geom)

        # return json.dumps(data['geom'])
