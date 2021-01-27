import cx_Oracle
import logging

log = logging.getLogger(__name__)


class Facta():

    def __init__(self, user, password, host):
        log.debug("Oracle client version: %s" % '.'.join(tuple(map(str, cx_Oracle.clientversion()))))
        self.conn = cx_Oracle.connect(user, password, host)
        log.debug("Connected to Oracle server version: %s" % self.conn.version)
