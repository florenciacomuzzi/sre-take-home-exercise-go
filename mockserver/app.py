import logging
from datetime import datetime, timezone

import os

from flask import Flask

from mockserver.common import get_uuid
from mockserver.http_metrics import HttpMetrics
from mockserver.routes import configure_routes

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    http_metrics = HttpMetrics()

    # Default config via environment vars (or fallback)
    app.config['WINDOW'] = float(os.getenv('FLAKY_WINDOW', 60))     # seconds
    app.config['UP_RATIO'] = float(
        os.getenv('FLAKY_UP_RATIO', 0.8))  # success fraction

    pid = os.getenv('PID', f'mockserver{get_uuid(8)}')

    configure_routes(app=app, http_metrics=http_metrics,
                     server_start_ts=datetime.now(timezone.utc), pid=pid)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
