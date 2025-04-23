import time
from datetime import datetime, timezone
from monitor.endpoint import is_up


def monitor_endpoints(endpoints, stats):
    for endpoint in endpoints:
        available = is_up(endpoint['url'], endpoint.get('method', 'GET'), endpoint.get('body'),
                          endpoint.get('headers'))

        stat = stats.get(endpoint['url'], {'available': 0, 'total': 0})

        stat['timestamp'] = datetime.now()

        stat['available'] += 1 if available else 0
        stat['total'] += 1

        stats[endpoint['url']] = stat

    return stats