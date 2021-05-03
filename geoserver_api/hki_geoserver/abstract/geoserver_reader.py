from django.conf import settings
from .geoserver_reader_json import GeoServer_Reader_json
from .geoserver_reader_xml import GeoServer_Reader_xml

class GeoServer_Reader(GeoServer_Reader_json if settings.USE_JSON_READER else GeoServer_Reader_xml):
    pass
