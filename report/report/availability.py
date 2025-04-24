from report.database import Database
from report.aggregations import get_availability_by_domain, \
    get_availability_by_domains, get_availability_by_server


class Metrics:
    """Availability as measured by monitor utility."""
    def __init__(self):
        self.db = Database()
        self.coll = 'http_metrics'

    def get_availability_by_server(self):
        pipeline = get_availability_by_server()
        results = self.db.aggregate(self.coll, pipeline)
        return results

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