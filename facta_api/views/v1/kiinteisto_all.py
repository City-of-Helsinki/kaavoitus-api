from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
import logging
from django.conf import settings
from django.http.response import HttpResponseNotFound
from ..serializers.v1 import KiinteistonDataV1Serializer
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI
from .rakennus import RakennusAPI
from geoserver_api import hki_geoserver
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class API(KiinteistoAPI, RakennusAPI):
    serializer_class = KiinteistonDataV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")
        ktunnus_to_use = self._format_kiinteistotunnus(kiinteistotunnus)
        if not ktunnus_to_use:
            return HttpResponseBadRequest("Need valid kiinteistotunnus!")
        if not request.auth:
            return HttpResponse(status=401)
        self.facta_creds = request.auth.access_facta
        if not self.facta_creds:
            return HttpResponseForbidden("No access!")

        owners, occupants = self.get_kiinteisto(ktunnus_to_use)

        if not owners and not occupants:
            return HttpResponseNotFound()

        naapurit = []
        geoserver_creds = request.auth.access_geoserver
        if geoserver_creds:
            # Confirmed access to GeoServer.
            # Go get the data!
            kt = hki_geoserver.Kiinteistotunnus(
                username=geoserver_creds.username, password=geoserver_creds.credential
            )
            kt_data = kt.get(kiinteistotunnus)
            neighbours = []
            if kt_data:
                t = hki_geoserver.Tontti(
                    username=geoserver_creds.username,
                    password=geoserver_creds.credential,
                )
                neighbours = t.list_of_neighbours(
                    kt_data, neigh_to_skip=[kiinteistotunnus]
                )

            if neighbours:
                for neighbour in neighbours:
                    neighbour_ktunnus = self._format_kiinteistotunnus(neighbour)
                    n_owners, n_occupants = self.get_kiinteisto(neighbour_ktunnus)
                    naapurit.append(
                        {
                            "kiinteistotunnus": neighbour_ktunnus,
                            "omistajat": n_owners,
                            "haltijat": n_occupants,
                            "rakennuksen_omistajat": self.get_rakennus(
                                neighbour_ktunnus
                            ),
                        }
                    )

        kiinteisto_data = {
            "kiinteistotunnus": ktunnus_to_use,
            "omistajat": owners,
            "haltijat": occupants,
            "naapurit": naapurit,
            "rakennuksen_omistajat": self.get_rakennus(ktunnus_to_use),
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kiinteisto_data)
        if not serializer.is_valid():
            log.error("Errors: %s" % str(serializer.errors))

            return HttpResponseServerError("Data not formatted correctly!")

        return JsonResponse(serializer.validated_data)

    def get_kiinteisto(self, ktunnus):
        # Confirmed access to Facta Oracle SQL.
        # Mocking?
        mock_dir = settings.FACTA_DB_MOCK_DATA_DIR

        cache_key = f'facta_api_kiinteisto_all_get_kiinteisto_owner_rows_{ktunnus}'
        owner_rows = cache.get(cache_key)

        if owner_rows is None:
            # Go get the data!
            if mock_dir:
                f_ko = hel_facta.KiinteistonOmistajat(mock_data_dir=mock_dir)
            else:
                f_ko = hel_facta.KiinteistonOmistajat(
                    user=self.facta_creds.username,
                    password=self.facta_creds.credential,
                    host=self.facta_creds.host_spec,
                )
            rows = f_ko.get_by_kiinteistotunnus(ktunnus)
            # if not rows:
            #    return HttpResponseNotFound()

            # Process result:
            owner_rows = []
            if rows:
                for row in rows:
                    # KiinteistonOmistajaV1Serializer.OWNER_TYPES
                    if row[14] == "10":  # C_LAJI
                        # Helsinki
                        owner_type = "H"
                    elif row[14] in ["8", "11"]:  # C_LAJI
                        # Govt. of Finland
                        owner_type = "F"
                    else:
                        # Private
                        owner_type = "P"

                    owner = {
                        "kiinteistotunnus": row[2],  # KIINTEISTOTUNNUS
                        "address": self._extract_omistaja_address(row),
                        "owner_home_municipality": row[17],  # C_KOTIKUNT
                        "property_owner_type": owner_type,
                        "y_tunnus": row[16],  # C_LYTUNN
                    }
                    owner_rows.append(owner)
                cache.set(cache_key, owner_rows, settings.FACTA_CACHE_TIMEOUT)

        cache_key = f'facta_api_kiinteisto_all_get_kiinteisto_occupant_rows_{ktunnus}'
        occupant_rows = cache.get(cache_key)

        if occupant_rows is None:
            if mock_dir:
                f_kh = hel_facta.KiinteistonHaltijat(mock_data_dir=mock_dir)
            else:
                f_kh = hel_facta.KiinteistonHaltijat(
                    user=self.facta_creds.username,
                    password=self.facta_creds.credential,
                    host=self.facta_creds.host_spec,
                )
            rows = f_kh.get_by_kiinteistotunnus(ktunnus)

            occupant_rows = []
            # Process result:
            if rows:
                for row in rows:
                    log.debug(row)
                    occupant = {
                        "kiinteistotunnus": row[2],  # KIINTEISTOTUNNUS
                        "address": self._extract_haltija_address(row),
                        "y_tunnus": row[23],  # C_LYTUNN
                    }
                    occupant_rows.append(occupant)
                cache.set(cache_key, occupant_rows, settings.FACTA_CACHE_TIMEOUT)

        return owner_rows, occupant_rows

    def get_rakennus(self, ktunnus):
        cache_key = f'facta_api_kiinteisto_all_get_rakennus_{ktunnus}'
        owner_rows = cache.get(cache_key)

        if owner_rows is None:
            mock_dir = settings.FACTA_DB_MOCK_DATA_DIR
            if mock_dir:
                f_ko = hel_facta.RakennuksenOmistajat(mock_data_dir=mock_dir)
            else:
                f_ko = hel_facta.RakennuksenOmistajat(
                    user=self.facta_creds.username,
                    password=self.facta_creds.credential,
                    host=self.facta_creds.host_spec,
                )
            rows = f_ko.get_by_kiinteistotunnus(ktunnus)

            owner_rows = []
            if rows:
                for row in rows:
                    owner = {
                        "kiinteistotunnus": row[1],  # C_KIINTEISTOTUNNUS
                        "address": self._extract_rakennuksen_omistaja_address(row),
                        "y_tunnus": row[14],  # C_LYTUNN
                    }
                    owner_rows.append(owner)
                cache.set(cache_key, owner_rows, settings.FACTA_CACHE_TIMEOUT)

        return owner_rows
