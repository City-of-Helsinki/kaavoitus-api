from rest_framework.views import APIView
import logging

log = logging.getLogger(__name__)


class KiinteistoAPI(APIView):
    @staticmethod
    def _format_kiinteistotunnus(kiinteistotunnus):
        if len(kiinteistotunnus) == 17 and kiinteistotunnus.count("-") == 3:
            # Looking good
            return kiinteistotunnus

        if len(kiinteistotunnus) == 14 and kiinteistotunnus.count("-") == 0:
            kt_out = "%s-%s-%s-%s" % (
                kiinteistotunnus[:3],
                kiinteistotunnus[3:6],
                kiinteistotunnus[6:10],
                kiinteistotunnus[10:],
            )
            log.debug(
                "Formatted kiinteistötunnus '%s' into valid format." % kiinteistotunnus
            )

            return kt_out

        # Fail, the input isn't valid
        return None

    @staticmethod
    def _extract_omistaja_address(row):
        address = {
            "first_names": row[11],  # C_ETUNIMET
            "last_name": row[10],  # C_SUKUNIMI
            "address": row[12],  # C_LAHIOSOITE
            "address2": row[24],  # C_YHTTIED1
            "zip_code": row[13],  # C_POSTINRO
            "city_fin": row[27],  # POSTITMP_FIN
            "city_swe": row[28],  # POSTITMP_SWE
        }

        return address

    @staticmethod
    def _extract_haltija_address(row):
        address = {
            "first_names": row[18],  # C_ETUNIMET
            "last_name": row[17],  # C_SUKUNIMI
            "address": row[19],  # C_LAHIOSOITE
            "address2": row[26],  # C_YHTTIED1
            "zip_code": row[20],  # C_POSTINRO
            "city_fin": row[27],  # POSTITMP_FIN
            "city_swe": row[28],  # POSTITMP_SWE
        }

        return address
