import cx_Oracle
import logging

log = logging.getLogger(__name__)


class Facta:
    table_name = None
    mocked = False

    def __init__(self, user=None, password=None, host=None, mock_data_dir=None):
        if not self.table_name:
            raise RuntimeError("Need to inherit this class.")

        if mock_data_dir:
            self.mocked = True
            self._mock_login(mock_data_dir)
        elif user and password and host:
            self.login(user, password, host)
        else:
            raise ValueError("Oracle DB connection or mocking needed!")

    def login(self, user, password, host):
        log.debug(
            "Oracle client version: %s"
            % ".".join(tuple(map(str, cx_Oracle.clientversion())))
        )
        self.conn = cx_Oracle.connect(user, password, host)
        log.debug("Connected to Oracle server version: %s" % self.conn.version)

    def _mock_login(self, mock_data_dir):
        from .mock_oracle import MockOracleConnection
        import os

        if not os.path.exists(mock_data_dir) or not os.path.isdir(mock_data_dir):
            raise ValueError("Bad mock data dir %s!" % mock_data_dir)
        self.conn = MockOracleConnection(mock_data_dir)
