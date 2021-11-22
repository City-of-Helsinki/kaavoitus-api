import os
import pickle
import sqlparse


class MockOracleConnection:
    def __init__(self, mock_data_dir):
        self.mock_dir = mock_data_dir

    def cursor(self):
        return MockOracleCursor(self.mock_dir)


class MockOracleCursor:
    def __init__(self, mock_data_dir):
        self.mock_dir = mock_data_dir
        self.data = None

    def execute(self, *args, **kwargs):
        self.data = None
        sql = args[0]
        parsed = sqlparse.parse(sql)
        if not parsed:
            raise ValueError("Bad SQL!")
        table = None

        # Find table name
        for part in parsed[0]:
            if isinstance(part, sqlparse.sql.Identifier):
                table = part.value
                break

        if not table:
            raise ValueError("Cannot parse table name from SQL!")

        # Check what to query for
        if kwargs:
            if len(kwargs) != 1:
                raise ValueError("Don't know how to handle this!")
            id = kwargs[list(kwargs.keys())[0]]
        else:
            id = None

        if not id:
            raise ValueError("Don't know PK id!")

        data_file = "%s/%s-%s.dat" % (self.mock_dir, table, id)
        if not os.path.exists(data_file):
            self.data = []
        else:
            self.data = self._load_resultset(data_file)

    def close(self):
        self.data = None

    def __iter__(self):
        yield from self.data

    def _load_resultset(self, data_file):
        data = pickle.load(open(data_file, "rb"))

        return data
