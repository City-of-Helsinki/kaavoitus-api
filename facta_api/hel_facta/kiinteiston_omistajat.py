from cx_Oracle import DatabaseError
import logging
from .abstract import Facta

log = logging.getLogger(__name__)


class KiinteistonOmistajat(Facta):

    def get_by_kiinteistotunnus(self, kiinteistotunnus):
        # Note:
        # KIINTEISTOTUNNUS == C_KUNTA - C_SIJAINTI - C_RYHMA - C_YKSIKKO
        sql = """
select
    KG_KKIINT,
    KG_KHALLYKS,
    KIINTEISTOTUNNUS,
    MAARAALATUNNUS,
    C_KUNTA, C_SIJAINTI, C_RYHMA, C_YKSIKKO,
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
        row = None
        # Docs: https://cx-oracle.readthedocs.io/en/latest/api_manual/cursor.html
        kt_cursor = self.conn.cursor()
        try:
            kt_cursor.execute(sql, kiinteistotunnus=kiinteistotunnus)
            if kt_cursor.rowcount > 1:
                raise RuntimeError("Too many rows returned! Expecting single PK-entry.")
            row = kt_cursor.fetchone()
        except DatabaseError as exc:
            err, = exc.args
            log.error("Oracle-Error-Code: %d" % err.code)
            log.error("Oracle-Error-Message: %s" % err.message)
        except Exception as exc:
            log.error("Query failed: %s" % exc)
        finally:
            kt_cursor.close()

        return row
