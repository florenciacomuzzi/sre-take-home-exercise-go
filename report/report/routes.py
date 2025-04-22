import time

from flask import request
from datetime import datetime

from mockserver.common import get_uuid


def configure_routes(app, db, pid):

    @app.route('/', methods=['GET', 'POST'])
    def health():
        uuid = get_uuid(12)
        request_data = {
            "pid": pid,
            "uuid": uuid,
            "type": "request",
            'url': request.url,
            'method': request.method,
            'headers': dict(request.headers),
            'timestamp': datetime.utcnow(),
            'data': request.get_json() if request.is_json else request.form.to_dict()
        }

        db.db.requests.insert_one(request_data)

        window = float(app.config['WINDOW'])
        up_ratio = float(app.config['UP_RATIO'])

        # time‑based cycling
        phase = time.time() % window
        response_data = {
            "pid": pid,
            "uuid": uuid,
            "type": "response",
            'timestamp': datetime.utcnow(),
        }

        if phase < up_ratio * window:
            response_data['status'] = 'success'
            response_data['message'] = 'OK'
            response_data['code'] = 200
            db.db.requests.insert_one(response_data)
            return 'OK', 200
        else:
            response_data['status'] = 'error'
            response_data['message'] = 'FAIL'
            response_data['code'] = 500
            db.db.requests.insert_one(response_data)
            return 'FAIL', 500
