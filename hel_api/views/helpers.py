import logging

from datetime import datetime
from django.conf import settings

log = logging.getLogger(__name__)


def build_apila_url(typenames, hankenumero, cql_filter):
    url = settings.APILA_URL \
          + "?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=" + typenames \
          + ("&CQL_FILTER=" + cql_filter if cql_filter else "") \
          + "(geom,querySingle('hel:Pinoalue','geom','hankenumero=''" + hankenumero + "'''))" \
          + "&outputFormat=application/json"
    return url


def format_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        log.error(f'Failed to parse date from value {date}')
        return date  # Return date with wrong format regardless


def sisallyta_vain_kaavaan_kuuluvat(leikkaavat, koskettavat):
    tunnukset = []
    for tunnus in leikkaavat:
        if tunnus not in koskettavat:
            tunnukset.append(tunnus)
    return tunnukset
