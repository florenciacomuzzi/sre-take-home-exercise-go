from mockserver.database import Database


class HttpMetrics:
    def __init__(self):
        self.db = Database()
        self.coll = 'http_metrics'

    def insert_request(self, record) -> None:
        self.db.insert_record(self.coll, record)

    def insert_response(self, record) -> None:
        self.db.insert_record(self.coll, record)
