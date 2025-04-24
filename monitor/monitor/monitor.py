import time
from datetime import datetime, timezone
from urllib.parse import urlparse
from monitor.endpoint import is_up
from monitor.metrics import HealthMetrics

def monitor_endpoints(endpoints, stats, health_metrics):
    for endpoint in endpoints:
        available = is_up(endpoint['url'], endpoint.get('method', 'GET'), endpoint.get('body'),
                          endpoint.get('headers'))
        ts = datetime.now()

        parsed_url = urlparse(endpoint['url'])
        domain = parsed_url.netloc.split(':')[0]  # Remove port number if present

        stat = stats.get(endpoint['url'], {
            'domain': domain,
            'url': endpoint['url'],
            'start': stats['start'],
            'total': 0,
            'available': 0,
        })

        stat['end'] = ts

        stat['available'] += 1 if available else 0
        stat['total'] += 1

        stats[endpoint['url']] = stat

        health_metrics.insert_stat(stat)

    return stats