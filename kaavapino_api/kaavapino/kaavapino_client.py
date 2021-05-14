import logging
import requests
from django.conf import settings

log = logging.getLogger(__name__)

PROJECT_PATH = "projects"
PROJECT_DETAILS_PATH = "simple"
PROJECT_CHANGES_PATH = "changes"


class KaavapinoClient:
    api_url = None
    api_key = None

    def __init__(self, api_key=None):
        assert settings.KAAVAPINO_API_URL, "KAAVAPINO_API_URL is not set"
        assert api_key, "KAAVAPINO API KEY is not set"
        self.api_url = settings.KAAVAPINO_API_URL
        self.api_key = api_key

    def _get(self, path):
        try:
            url = "{:s}/{:s}".format(self.api_url, path)
            log.debug("GET from Kaavapino: %s", url)
            resp = requests.get(
                url,
                headers={"Authorization": "Token %s" % self.api_key},
            )
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 404:
                return {}
            else:
                raise Exception(resp)
        except Exception as e:
            log.warning("Kaavapino api request failed: %s" % e)
            raise e

    def get_projects(self, pinonro):
        return self._get(
            "{:s}/{:d}/{:s}/".format(PROJECT_PATH, int(pinonro), PROJECT_DETAILS_PATH)
        )

    def get_projects_changes(self, timestamp):
        return self._get(
            "{:s}/{:s}/{:d}/".format(PROJECT_PATH, PROJECT_CHANGES_PATH, int(timestamp))
        )
