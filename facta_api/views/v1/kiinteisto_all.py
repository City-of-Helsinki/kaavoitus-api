from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
import logging
from django.conf import settings
from ..serializers.v1 import KiinteistonDataV1Serializer
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI
from geoserver_api import hki_geoserver

log = logging.getLogger(__name__)


class API(KiinteistoAPI):
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
                    n_owners, n_occupants = self.get_kiinteisto(neighbour)
                    naapurit.append(
                        {
                            "kiinteistotunnus": neighbour,
                            "omistajat": n_owners,
                            "haltijat": n_occupants,
                        }
                    )

        kiinteisto_data = {
            "kiinteistotunnus": ktunnus_to_use,
            "omistajat": owners,
            "haltijat": occupants,
            "naapurit": naapurit,
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
        occupant_rows = []
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
                }
                owner_rows.append(owner)

        if mock_dir:
            f_kh = hel_facta.KiinteistonHaltijat(mock_data_dir=mock_dir)
        else:
            f_kh = hel_facta.KiinteistonHaltijat(
                user=self.facta_creds.username,
                password=self.facta_creds.credential,
                host=self.facta_creds.host_spec,
            )
        rows = f_kh.get_by_kiinteistotunnus(ktunnus)

        # Process result:
        if rows:
            for row in rows:
                log.debug(row)
                occupant = {
                    "kiinteistotunnus": row[2],  # KIINTEISTOTUNNUS
                    "address": self._extract_haltija_address(row),
                }
                occupant_rows.append(occupant)

        return owner_rows, occupant_rows
