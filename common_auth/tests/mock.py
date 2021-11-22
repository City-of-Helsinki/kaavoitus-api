class OracleCursorMock:
    def __init__(self):
        self.data = []

    def execute(self, *args, **kwargs):
        return []

    def close(self):
        pass

    def __iter__(self):
        yield from self.data


class OracleConnMock:
    def cursor():
        return OracleCursorMock()
