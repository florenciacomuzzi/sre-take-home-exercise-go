import os
import time

from flask import Flask, request, jsonify
from mock_server.database import Database
from datetime import datetime

app = Flask(__name__)
db = Database()

# Default config via environment vars (or fallback)
app.config['WINDOW']     = float(os.getenv('FLAKY_WINDOW', 60))     # seconds
app.config['UP_RATIO']   = float(os.getenv('FLAKY_UP_RATIO', 0.8))  # success fraction

@app.route('/', methods=['GET', 'POST'])
def health():
    request_data = {
        "type": "request",
        'url': request.url,
        'method': request.method,
        'headers': dict(request.headers),
        'timestamp': datetime.utcnow(),
        'data': request.get_json() if request.is_json else request.form.to_dict()
    }

    # Log request to MongoDB
    db.db.requests.insert_one(request_data)

    window   = float(app.config['WINDOW'])
    up_ratio = float(app.config['UP_RATIO'])

    # time‑based cycling
    phase = time.time() % window
    response_data = {
        "type": "response",
        'url': request.url,
        'timestamp': datetime.utcnow(),
        'data': request.get_json() if request.is_json else request.form.to_dict()
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
        db.db.requests.insert_one(response_data)
        return 'FAIL', 500

if __name__ == '__main__':
    app.run(debug=True) 