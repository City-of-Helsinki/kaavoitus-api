from cx_Oracle import DatabaseError
import logging
from .abstract import Facta
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class Rakennuskiellot(Facta):
    table_name = "MV_KIINTEISTON_RAKKIELLOT"

    def get_by_kiinteistotunnus(self, kiinteistotunnus):
        # Note:
        # KIINTEISTOTUNNUS == C_KUNTA - C_SIJAINTI - C_RYHMA - C_YKSIKKO
        sql = """
select
    KG_KRAKKIEL,
    KG_KKIINT,
    C_KUNTA,
    C_SIJAINTI,
    C_RYHMA,
    C_YKSIKKO,
    C_KIINTEISTO,
    C_TUNNUS,
    C_POIKPAATPVM,
    C_KOKOS,
    C_ANTAJA,
    C_JATKAMPVM,
    C_LAATU,
    C_VOIMPVM,
    C_PAATPVM,
    C_PAATOSPVM,
    C_NIMI,
    C_KTJ_MILLOIN,
    C_SIJKUNTA,
    C_HALLINTAYKSIKKOTUNNUS,
    C_HALLKIRJ,
    C_HALLTUNN
FROM
    MV_KIINTEISTON_RAKKIELLOT
WHERE
    C_KIINTEISTO = :kiinteistotunnus
"""

        cache_key = f'facta_api_rakennuskiellot_get_by_kiinteistotunnus_{kiinteistotunnus}'
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
