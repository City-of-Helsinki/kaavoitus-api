import logging

log = logging.getLogger(__name__)


def format_kiinteistotunnus(kiinteistotunnus):
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
