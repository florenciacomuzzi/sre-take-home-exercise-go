from flask import Flask
from datetime import datetime

from report.database import Database
from report.routes import configure_routes


def create_app():
    # pid = os.environ.get('PID', f'mockserver{get_uuid(8)}')
    pid = 'reporter'
    app = Flask(__name__)
    db = Database()

    # Add datetime filter
    @app.template_filter('datetime')
    def format_datetime(value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value

    configure_routes(app, db, pid)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
