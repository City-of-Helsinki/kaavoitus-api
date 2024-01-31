from owslib.wfs import WebFeatureService

VERSION = "2.0.0"
wfs_list = {}


def get_or_init_wfs(url, username=None, password=None):
    try:
        wfs = wfs_list[(url, username, password)]
    except KeyError:
        wfs = WebFeatureService(url, version=VERSION, username=username, password=password)
        wfs_list[(url, username, password)] = wfs
    return wfs
