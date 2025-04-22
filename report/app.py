import os

from flask import Flask

from report.database import Database
from report.routes import configure_routes


def create_app():
    # pid = os.environ.get('PID', f'mockserver{get_uuid(8)}')
    pid = 'mockserver0'
    app = Flask(__name__)
    db = Database()

    configure_routes(app, db, pid)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
