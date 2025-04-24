from monitor.database import Database
# from monitor.aggregations import get_uptime_percentage, get_unique_pids


class HealthMetrics:
    def __init__(self):
        self.db = Database()
        self.coll = 'health_metrics'

    # def get_all_pids(self):
    #     """Get all unique PIDs from the database."""
    #     pipeline = get_unique_pids()
    #     results = self.db.aggregate(self.coll, pipeline)
    #     return [doc['_id'] for doc in results]

    # def get_uptime_percentage(self, pid, start=None, end=None):
    #     pipeline = get_uptime_percentage(pid, start, end)
    #     results = self.db.aggregate(self.coll, pipeline)
    #     results = results[0]
    #     results['pid'] = pid
    #     return results

    # def get_uptime_percentages(self):
    #     """Get all metrics for all PIDs."""
    #     all_metrics = []
    #     pids = self.get_all_pids()
    #     for pid in pids:
    #         metrics = self.get_uptime_percentage(pid)
    #         all_metrics.append(metrics)
    #     return all_metrics

    def insert_stat(self, record) -> None:
        self.db.insert_record(self.coll, record)