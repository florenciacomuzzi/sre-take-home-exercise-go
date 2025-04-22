import time

from flask import request, jsonify, render_template
from datetime import datetime

from report.aggregations import get_uptime_percentage
from report.metrics import Metrics


def configure_routes(app, db, pid):

    @app.route('/', methods=['GET', 'POST'])
    def report():
        metrics = Metrics()
        pids = metrics.get_all_pids()

        # Get metrics for all PIDs
        results = {}
        for pid in pids:
            results[pid] = metrics.get_uptime_percentage(pid)

        # Return JSON for API requests
        if request.headers.get('Accept') == 'application/json':
            return jsonify(results)

        # Return HTML template for browser requests
        return render_template('metrics.html', metrics_by_pid=results)
