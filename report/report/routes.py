from flask import request, jsonify, render_template

from report.availability import Metrics as HttpMetrics
from report.availability import HealthMetrics


def configure_routes(app, db, pid):

    @app.route('/', methods=['GET', 'POST'])
    def report():
        metrics = HttpMetrics()
        results = metrics

        health_metrics = HealthMetrics()

        # Return JSON for API requests
        if request.headers.get('Accept') == 'application/json':
            return jsonify(results)

        # Return HTML template for browser requests
        return render_template('metrics.html', metrics=results, domain_metrics=health_metrics)
