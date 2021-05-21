from rest_framework.views import APIView
import logging

log = logging.getLogger(__name__)


class RakennusAPI(APIView):
    @staticmethod
    def _extract_rakennuksen_omistaja_address(row):
        address = {
            "first_names": row[8],  # C_ETUNIMET
            "last_name": row[7],  # C_SUKUNIMI
            "address": row[9],  # C_LAHIOSOITE
            "address2": row[16],  # C_YHTTIED1
            "zip_code": row[10],  # C_POSTINRO
            "city_fin": row[17],  # POSTITMP_FIN
            "city_swe": row[18],  # POSTITMP_SWE
        }

        return address
