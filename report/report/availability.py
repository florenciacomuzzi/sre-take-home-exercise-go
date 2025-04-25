from datetime import tzinfo, datetime, timezone, timedelta

from report.database import Database
from report.aggregations import (get_availability_by_server,
                                 get_availability_by_domain_since)

from report import aggregations


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

    def get_availability_by_domain(self):
        pipeline = aggregations.get_availability_by_domain()
        results = self.db.aggregate(self.coll, pipeline)
        return results

    def get_availability_by_domain_since(self, dt):
        pipeline = get_availability_by_domain_since(dt)
        results = self.db.aggregate(self.coll, pipeline)
        return results

    def get_alltime_availability(self):
        return self.get_availability_by_domain()

    def get_alltime_and_last30mins_availability(self):
        alltime = self.get_availability_by_domain()
        start = datetime.now(timezone.utc) - timedelta(minutes=30)
        last30mins = self.get_availability_by_domain_since(start)
        results = {
            ''
            'alltime': alltime,
            'last30mins': last30mins
        }
        return alltime, last30mins
