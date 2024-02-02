from geoserver_api.hki_geoserver.abstract.geoserver_reader import GeoServer_Reader, GeoServer_Reader_xml, GeoServer_Reader_json


class GeoserverReaderJson(GeoServer_Reader_json):
    use_auth = False
    use_opendata = True
    layername = "hel:Kiinteisto_alue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "id": "int",
        },
        "required": ["id"],
    }


class GeoserverReaderXml(GeoServer_Reader_xml):
    use_auth = False
    use_opendata = True
    layername = "hel:Kiinteisto_alue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "id": "int",
        },
        "required": ["id"],
    }


class TestGeoserverReader:

    def test_geoserver_reader_json(self):
        reader = GeoserverReaderJson()
        fields_to_retrieve = reader._schema_to_fieldlist()
        num_returned, result = reader.query(
            fields_to_retrieve, filter={"hankenumero": "4428_4"}
        )
        assert result is not None

    def test_geoserver_reader_xml(self):
        reader = GeoserverReaderXml()
        fields_to_retrieve = reader._schema_to_fieldlist()
        num_returned, result = reader.query(
            fields_to_retrieve, filter={"hankenumero": "4428_4"}
        )
        assert result is not None
