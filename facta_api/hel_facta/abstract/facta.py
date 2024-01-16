import logging
from .facta_session_pool import session_pool

log = logging.getLogger(__name__)


class Facta:
    table_name = None
    mocked = False
    conn = None

    def __init__(self, mock_data_dir=None):
        if not self.table_name:
            raise RuntimeError("Need to inherit this class.")

        if mock_data_dir:
            self.mocked = True
            self._mock_login(mock_data_dir)
        elif session_pool:
            self.conn = session_pool.acquire()
        else:
            raise ValueError("Oracle DB connection or mocking needed!")

    def __del__(self):
        if self.conn:
            session_pool.release(self.conn)

    def _mock_login(self, mock_data_dir):
        from .mock_oracle import MockOracleConnection
        import os

        if not os.path.exists(mock_data_dir) or not os.path.isdir(mock_data_dir):
            raise ValueError("Bad mock data dir %s!" % mock_data_dir)
        self.conn = MockOracleConnection(mock_data_dir)
