from cx_Oracle import DatabaseError
import logging
from .abstract import Facta

log = logging.getLogger(__name__)


class KiinteistonHaltijat(Facta):
    table_name = "MV_KIINTEISTON_HALTIJAT"

    def get_by_kiinteistotunnus(self, kiinteistotunnus):
        # Note:
        # KIINTEISTOTUNNUS == C_KUNTA - C_SIJAINTI - C_RYHMA - C_YKSIKKO
        sql = """
select
    KG_KKIINT,
    KG_KHALLYKS,
    KIINTEISTOTUNNUS,
    HALLINTAYKSIKKO,
    C_KUNTA, C_SIJAINTI, C_RYHMA, C_YKSIKKO,
    C_HALLKIRJ,
    C_HALLTUNN,
    C_VUOLOPVM,
    C_VSOPNRO,
    C_ALKIRPVM,
    C_VUOALPVM,
    C_VSIIRPVM,
    C_VUOKRAMK,
    C_MYYHINTA,
    C_SUKUNIMI,
    C_ETUNIMET,
    C_LAHIOSOITE,
    C_POSTINRO,
    C_LAJI,
    C_SOTU,
    C_LYTUNN,
    C_KOTIKUNT,
    C_ONKO_KUOLLUT,
    C_YHTTIED1,
    POSTITMP_FIN,
    POSTITMP_SWE,
    C_ONKO_ASIAMIES,
    C_VUOKRATUNN,
    C_SIJKUNTA,
    C_ONKO_ULKOMAINEN_OSOITE,
    C_ULKOMAINEN_OSOITE1,
    C_ULKOMAINEN_OSOITE2,
    C_ULKOMAINEN_OSOITE_MAA
FROM
    MV_KIINTEISTON_HALTIJAT
WHERE
    KIINTEISTOTUNNUS = :kiinteistotunnus
"""
        rows = []
        # Docs: https://cx-oracle.readthedocs.io/en/latest/api_manual/cursor.html
        kt_cursor = self.conn.cursor()
        try:
            kt_cursor.execute(sql, kiinteistotunnus=kiinteistotunnus)
            for row in kt_cursor:
                rows.append(row)
        except DatabaseError as exc:
            err, = exc.args
            log.error("Oracle-Error-Code: %d" % err.code)
            log.error("Oracle-Error-Message: %s" % err.message)
            raise RuntimeError("Oracle-Error-Code: %d, Oracle-Error-Message: %s" % (err.code, err.message))
        except Exception as exc:
            log.error("Query failed: %s" % exc)
            raise RuntimeError("Query failed: %s" % exc)
        finally:
            kt_cursor.close()

        return rows
