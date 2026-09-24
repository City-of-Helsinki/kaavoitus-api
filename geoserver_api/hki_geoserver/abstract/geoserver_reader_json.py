#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

# This code adapted from:
# https://github.com/geopython/OWSLib/blob/master/examples/wms-getfeatureinfo.py

import copy
from .geoserver_wfs_helper import get_or_init_wfs
import logging
import lxml.etree as etree
from lxml.builder import ElementMaker
from pydov.util import location
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform
import json

log = logging.getLogger(__name__)

HELSINKI_GEOSERVER_OPENDATA_URL = "https://kartta.hel.fi/ws/geoserver/avoindata/wfs"
HELSINKI_GEOSERVER_INTERNAL_URL = "http://apila.hel.fi/gis/hel/wfs"
HELSINKI_GEOSERVER_OLD_URL = "https://kartta.hel.fi/ws/geoserver/helsinki/wfs"

# GML 3.2 namespace
GML_NS = "http://www.opengis.net/gml/3.2"
NSMAP = {"gml": GML_NS}

class GeoServer_Reader_json:
    wfs = None
    geo_url = None
    layername = None
    schema = None
    use_auth = None
    username = None
    password = None
    use_opendata = False

    use_old_url = False

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
            url_to_use = HELSINKI_GEOSERVER_INTERNAL_URL

        if self.use_opendata:
            url_to_use = HELSINKI_GEOSERVER_OPENDATA_URL

        if self.use_old_url:
            url_to_use = HELSINKI_GEOSERVER_OLD_URL

        if self.geo_url:
            if url_to_use != self.geo_url:
                self.wfs = None
        if self.wfs:
            return

        self.geo_url = url_to_use

        if self.use_auth or self.use_old_url:
            wfs = get_or_init_wfs(self.geo_url, self.username, self.password)
        else:
            wfs = get_or_init_wfs(self.geo_url)

        self.wfs = wfs

        return wfs

    def get_schema(self):
        self._init_wfs()
        layer_schema = self.wfs.get_schema(self.layername)

        return layer_schema

    def query(
        self, fields, filter={}, return_single_result=True, limit_results_to=2500
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

        returned = 0
        kdata_out = []
        try:
            response = self.wfs.getfeature(
                typename=self.layername,
                # srsname='urn:ogc:def:crs:EPSG::4326',
                # srsname='EPSG:3879',
                filter=filter_fes,
                startindex=0,
                method="post",
                outputFormat="json",
            )
        except Exception as e:
            log.warning(e)
            # Don't die
            return returned, kdata_out

        raw = json.loads(response.read())
        # log.info(raw)
        returned = raw.get("numberReturned")
        if limit_results_to and returned > limit_results_to:
            log.error("Argh! Too much data.")
            raise ValueError(
                "Too much data. Faulty filter! Expecting less than %d, but got %d."
                % (limit_results_to, returned)
            )
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
        geometry_data = data["geom"][0].get("geometry")

        if not geometry_data:
            raise ValueError("Geometry missing!")

        geom = shape(geometry_data)

        srs_name = data["srs"]

        # ---------------------------------------------------------
        # Build MultiSurface
        # ---------------------------------------------------------
        root = etree.Element(
            f"{{{GML_NS}}}MultiSurface",
            nsmap={"gml": GML_NS},
        )

        root.set(
            f"{{{GML_NS}}}id",
            data["id"],
        )

        root.set(
            "srsName",
            srs_name,
        )

        def add_ring(parent, ring):
            linear_ring = etree.SubElement(
                parent,
                f"{{{GML_NS}}}LinearRing",
            )

            pos_list = etree.SubElement(
                linear_ring,
                f"{{{GML_NS}}}posList",
            )

            pos_list.set("srsDimension", "2")

            coords = []

            for x, y in ring.coords:
                coords.extend([str(x), str(y)])

            pos_list.text = " ".join(coords)

        def add_polygon(parent, polygon, polygon_id):

            polygon_el = etree.SubElement(
                parent,
                f"{{{GML_NS}}}Polygon",
            )

            polygon_el.set(
                f"{{{GML_NS}}}id",
                polygon_id,
            )

            # Exterior
            exterior = etree.SubElement(
                polygon_el,
                f"{{{GML_NS}}}exterior",
            )

            add_ring(
                exterior,
                polygon.exterior,
            )

            # Holes
            for interior_ring in polygon.interiors:

                interior = etree.SubElement(
                    polygon_el,
                    f"{{{GML_NS}}}interior",
                )

                add_ring(
                    interior,
                    interior_ring,
                )

        # ---------------------------------------------------------
        # Polygon / MultiPolygon
        # ---------------------------------------------------------

        if geom.geom_type == "Polygon":

            # Replace MultiSurface with Polygon for a single polygon
            root = etree.Element(
                f"{{{GML_NS}}}Polygon",
                nsmap={"gml": GML_NS},
            )

            root.set(
                f"{{{GML_NS}}}id",
                data["id"],
            )

            root.set(
                "srsName",
                srs_name,
            )

            add_polygon(
                root,
                geom,
                data["id"],
            )

        elif geom.geom_type == "MultiPolygon":

            for i, polygon in enumerate(geom.geoms):

                member = etree.SubElement(
                    root,
                    f"{{{GML_NS}}}surfaceMember",
                )

                add_polygon(
                    member,
                    polygon,
                    f"{data['id']}.{i + 1}",
                )

        else:
            raise ValueError(
                f"Unsupported geometry type: {geom.geom_type}"
            )

        gml = etree.tostring(
            root,
            encoding="unicode",
        )

        return location.GmlObject(gml)

    def convert_data(self, data):
        return self._json_to_gml(data)

    def get_geometry(self, data):
        # create a geometry from coordinates
        new_geom = copy.deepcopy(data["geom"])
        geom = shape(new_geom[0]["geometry"])

        # Determine source CRS
        if data["srs"]:
            # Extract EPSG code from SRS string
            if "EPSG" in data["srs"]:
                source_epsg = data["srs"].split("EPSG")[-1].strip(":").strip()
            else:
                source_epsg = "3879"  # fallback
        else:
            # Fallback to the crs that should be in use
            source_epsg = "3879"

        # Create coordinate transformer from source CRS to WGS84 (EPSG:4326)
        # PyProj uses "always_xy=True" to ensure (lon, lat) order regardless of CRS definition
        transformer = Transformer.from_crs(
            f"EPSG:{source_epsg}",
            "EPSG:4326",
            always_xy=True
        )

        transformed_geom = transform(transformer.transform, geom)

        # Convert GeoJSON coordinates from [lng, lat] to [lat, lng]
        geojson = mapping(transformed_geom)

        def swap_coordinates(coords):
            if isinstance(coords[0], (float, int)):
                lng, lat = coords
                return [lat, lng]

            return [swap_coordinates(coord) for coord in coords]

        geojson["coordinates"] = swap_coordinates(geojson["coordinates"])
        new_geom[0]["geometry"] = geojson

        return new_geom