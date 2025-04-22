import os

from flask import Flask

from mockserver.common import get_uuid
from mockserver.database import Database
from mockserver.routes import configure_routes

def create_app():
    pid = os.environ.get('PID', f'mockserver{get_uuid(8)}')
    app = Flask(__name__)
    db = Database()

    # Default config via environment vars (or fallback)
    app.config['WINDOW']     = float(os.getenv('FLAKY_WINDOW', 60))     # seconds
    app.config['UP_RATIO']   = float(os.getenv('FLAKY_UP_RATIO', 0.8))  # success fraction

    configure_routes(app, db, pid)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 