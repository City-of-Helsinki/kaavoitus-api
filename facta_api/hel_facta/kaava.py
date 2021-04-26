from cx_Oracle import DatabaseError
import logging
from .abstract import Facta

log = logging.getLogger(__name__)


class Kaava(Facta):
    table_name = "MV_KAAVA"

    def get_by_kaavatunnus(self, kaavatunnus):
        sql = """
select
    KG_KKAAVA
    C_KAAVTUNN
    C_KIRJTUNN
    C_LISATUNN
    C_KAAVATUNNUS
    C_KAAVLAJI
    C_TYONIMI
    C_SAILMERK
    C_KAAVATIL
    C_VAHVPTEK
    C_LAINVPVM
    C_VOIMPVM
    C_NIMI
    C_KTJ_MILLOIN
    C_KUNTA
    C_NIMIJATKO
    C_KMERKPAATOS
    C_VAHPVM
    C_HUOM
    I_LASKPALA
    C_AJANMUK
    C_AJANMUK_PAIV
    I_VOIM_PALA
FROM
    MV_KAAVA
WHERE
    C_KAAVATUNNUS = :kaavatunnus
"""
        rows = []
        # Docs: https://cx-oracle.readthedocs.io/en/latest/api_manual/cursor.html
        kt_cursor = self.conn.cursor()
        try:
            kt_cursor.execute(sql, kaavatunnus=kaavatunnus)
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
