from monitor.database import Database


class HealthMetrics:
    def __init__(self):
        self.db = Database()
        self.coll = 'health_metrics'

    def insert_stat(self, record) -> None:
        self.db.insert_record(self.coll, record)