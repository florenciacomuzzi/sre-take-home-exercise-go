from report.database import Database
from report.aggregations import get_uptime_percentage, get_unique_pids, get_availability_by_domain, \
    get_availability_by_domains


class Metrics:
    """Availability as measured by monitor utility."""
    def __init__(self):
        self.db = Database()
        self.coll = 'availability'

    def get_all_pids(self):
        """Get all unique PIDs from the database."""
        pipeline = get_unique_pids()
        results = self.db.aggregate(self.coll, pipeline)
        return [doc['_id'] for doc in results]

    def get_uptime_percentage(self, pid, start=None, end=None):
        pipeline = get_uptime_percentage(pid, start, end)
        results = self.db.aggregate(self.coll, pipeline)
        results = results[0]
        results['pid'] = pid
        return results

    def get_uptime_percentages(self):
        """Get all metrics for all PIDs."""
        all_metrics = []
        pids = self.get_all_pids()
        for pid in pids:
            metrics = self.get_uptime_percentage(pid)
            all_metrics.append(metrics)
        return all_metrics


class HealthMetrics:
    """Availability as measured by monitor utility."""
    def __init__(self):
        self.db = Database()
        self.coll = 'health_metrics'

    def get_availability_by_domain(self, domain):
        pipeline = get_availability_by_domain(domain)
        results = self.db.aggregate(self.coll, pipeline)
        return results

    def get_availability_by_domains(self):
        pipeline = get_availability_by_domains()
        results = self.db.aggregate(self.coll, pipeline)
        return results