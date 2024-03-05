from geoserver_api.hki_geoserver.abstract.geoserver_reader import GeoServer_Reader, GeoServer_Reader_xml, GeoServer_Reader_json


class GeoserverReaderJson(GeoServer_Reader_json):
    use_auth = False
    use_opendata = True
    layername = "hel:Kiinteisto_alue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "datanomistaja": "string",
            "id": "int",
            "kiinteisto": "string",
            "kiinteistotunnus": "string",
            "kunta": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "paivitetty_tietopalveluun": "date",
            "rekisterointipvm": "date",
            "ryhma": "string",
            "sijaintialue": "string",
            "yksikko": "string",
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
            "datanomistaja": "string",
            "id": "int",
            "kiinteisto": "string",
            "kiinteistotunnus": "string",
            "kunta": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "paivitetty_tietopalveluun": "date",
            "rekisterointipvm": "date",
            "ryhma": "string",
            "sijaintialue": "string",
            "yksikko": "string",
        },
        "required": ["id"],
    }


convertable_data = {
    "id": 123,
    "srs": "urn:ogc:def:crs:EPSG::0123",
    "geom": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [24.9320125579834, 60.17221176544357],
                        [24.933841824531555, 60.17221176544357],
                        [24.933841824531555, 60.17283879431961],
                        [24.9320125579834, 60.17283879431961],
                        [24.9320125579834, 60.17221176544357],
                    ]
                ],
            },
            "properties": {"id": "Hankerajaukset_alue_kaavahanke.001"},
        }
    ]
}


class TestGeoserverReader:

    def test_geoserver_reader_json(self):
        reader = GeoserverReaderJson()
        reader.set_logging_level()

        wfs_schema = reader.get_schema()
        assert wfs_schema is not None

        fields_to_retrieve = reader._schema_to_fieldlist()
        num_returned, result = reader.query(
            fields_to_retrieve, filter={"kiinteistotunnus": "09101499010100"}
        )
        assert result is not None

        gml_polygon = reader.convert_data(convertable_data)
        assert gml_polygon is not None

    def test_geoserver_reader_xml(self):
        reader = GeoserverReaderXml()
        reader.set_logging_level()

        wfs_schema = reader.get_schema()
        assert wfs_schema is not None

        fields_to_retrieve = reader._schema_to_fieldlist()
        num_returned, result = reader.query(
            fields_to_retrieve, filter={"hankenumero": "09101499010100"}
        )
        assert result is not None

        gml_polygon = reader.convert_data(convertable_data)
        assert gml_polygon is not None