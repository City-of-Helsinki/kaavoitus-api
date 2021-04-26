from cx_Oracle import DatabaseError
import logging
from .abstract import Facta

log = logging.getLogger(__name__)


class Kiinteisto(Facta):
    table_name = "MV_KIINTEISTO"

    def get_by_kiinteistotunnus(self, kiinteistotunnus):
        # Note:
        # KIINTEISTOTUNNUS == C_KUNTA - C_SIJAINTI - C_RYHMA - C_YKSIKKO
        sql = """
select
    KG_KKIINT
    C_KUNTA
    C_SIJAINTI
    C_RYHMA
    C_YKSIKKO
    KIINTEISTOTUNNUS
    I_PKOORD
    I_IKOORD
    I_XKOORD
    I_YKOORD
    C_REKLAJI
    C_OLOTILA
    C_NIMI
    C_KAYTTOTA
    C_KTARSEL
    I_KOKOPALA
    I_MAAPALA
    I_VESIPALA
    I_LASKPALA
    C_REKPVM
    C_POISTPVM
    KG_YLEKIINT
    C_KAAVATJLAJI
    C_PALSTAN_PINTAALA
    C_PALSTAN_REKPVM
    C_REKPVMLAJI
    C_KTJ_REKLAJI
    C_OSALUKU
    C_MANTTAALI
    C_KTJ_KAYTTOTA
    C_KTJ_MHKAYTTOTA
    C_KTJ_KMHTARSEL
    C_KTJ_MILLOIN
    C_ARKISNRO
    C_POISTPVMLAJI
    KG_KHALLYKS
    C_VSOPNRO
    C_ALKIRPVM
    C_VUOALPVM
    C_VUOLOPVM
    C_VSIIRPVM
    C_VUOKRAMK
    C_MYYHINTA
    C_LISATIET
    C_KATUKKOD
    C_PALSTAN_MAAPALA
    C_PALSTAN_VESIPALA
    I_NKOORD
    I_EKOORD
    C_SIJKUNTA
    I_NKOORD_TM35FIN
    I_EKOORD_TM35FIN
FROM
    MV_KIINTEISTO
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
