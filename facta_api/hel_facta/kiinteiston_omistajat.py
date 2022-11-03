from cx_Oracle import DatabaseError
import logging
from .abstract import Facta
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class KiinteistonOmistajat(Facta):
    table_name = "MV_KIINTEISTON_OMISTAJAT"

    def get_by_kiinteistotunnus(self, kiinteistotunnus):
        # Note:
        # KIINTEISTOTUNNUS == C_KUNTA - C_SIJAINTI - C_RYHMA - C_YKSIKKO
        sql = """
select
    KG_KKIINT,
    KG_KHALLYKS,
    KIINTEISTOTUNNUS,
    MAARAALATUNNUS,
    C_KUNTA,
    C_SIJAINTI,
    C_RYHMA,
    C_YKSIKKO,
    C_HALLKIRJ,
    C_HALLTUNN,
    C_SUKUNIMI,
    C_ETUNIMET,
    C_LAHIOSOITE,
    C_POSTINRO,
    C_LAJI,
    C_SOTU,
    C_LYTUNN,
    C_KOTIKUNT,
    C_ONKO_KUOLLUT,
    C_LAINHPVM,
    C_PYKALA,
    C_SAANTPVM,
    C_OSUUS,
    I_JARJNRO,
    C_YHTTIED1,
    C_RATKAISU,
    C_RATKAISUPVM,
    POSTITMP_FIN,
    POSTITMP_SWE,
    C_ONKO_ASIAMIES,
    C_SAANTOSELITYS,
    C_SAALAATU,
    C_ASIANUMERO,
    C_ASIANLAATU,
    C_SIJKUNTA,
    C_ONKO_ULKOMAINEN_OSOITE,
    C_ULKOMAINEN_OSOITE1,
    C_ULKOMAINEN_OSOITE2,
    C_ULKOMAINEN_OSOITE_MAA
FROM
    MV_KIINTEISTON_OMISTAJAT
WHERE
    KIINTEISTOTUNNUS = :kiinteistotunnus
"""

        cache_key = f'facta_api_kiinteiston_omistajat_get_by_kiinteistotunnus_{kiinteistotunnus}'
        rows = cache.get(cache_key)

        if rows is None:
            rows = []
            # Docs: https://cx-oracle.readthedocs.io/en/latest/api_manual/cursor.html
            kt_cursor = self.conn.cursor()
            try:
                kt_cursor.execute(sql, kiinteistotunnus=kiinteistotunnus)
                for row in kt_cursor:
                    rows.append(row)
                cache.set(cache_key, rows, settings.FACTA_CACHE_TIMEOUT)
            except DatabaseError as exc:
                (err,) = exc.args
                log.error("Oracle-Error-Code: %d" % err.code)
                log.error("Oracle-Error-Message: %s" % err.message)
                raise RuntimeError(
                    "Oracle-Error-Code: %d, Oracle-Error-Message: %s"
                    % (err.code, err.message)
                )
            except Exception as exc:
                log.error("Query failed: %s" % exc)
                raise RuntimeError("Query failed: %s" % exc)
            finally:
                kt_cursor.close()

        return rows
