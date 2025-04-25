import time
import random

from flask import request
from datetime import datetime, timezone

from mockserver.common import get_uuid

from mockserver.config import Config

from mockserver.common import get_domain, clean_url


def random_successful_code():
    """Generate a random successful HTTP status code between 200 and 299."""
    return random.randint(200, 299)


def random_error_code():
    """Generate a random HTTP error code (4xx or 5xx).

    Returns:
        int: A random HTTP error code from common error codes
    """
    error_codes = [
        # 4xx Client Errors
        400,  # Bad Request
        401,  # Unauthorized
        403,  # Forbidden
        404,  # Not Found
        405,  # Method Not Allowed
        408,  # Request Timeout
        409,  # Conflict
        413,  # Payload Too Large
        429,  # Too Many Requests
        # 5xx Server Errors
        500,  # Internal Server Error
        501,  # Not Implemented
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
        507,  # Insufficient Storage
    ]
    return random.choice(error_codes)


def configure_routes(*, app, http_metrics, pid, server_start_ts=None):

    @app.route('/', methods=['GET', 'POST'])
    def health():
        print(f"PID: {pid}")
        uuid = get_uuid(12)
        domain = get_domain(request.url)
        url = clean_url(request.url)
        request_data = {
            "pid": pid,
            "uuid": uuid,
            "type": "request",
            'domain': domain,
            'url': url,
            'method': request.method,
            'headers': dict(request.headers),
            'server_start_ts': server_start_ts,
            'timestamp': datetime.now(timezone.utc),
            'data': request.get_json() if request.is_json else request.form.to_dict()
        }

        http_metrics.insert_request(request_data)

        window = float(app.config['WINDOW'])
        up_ratio = float(app.config['UP_RATIO'])

        # time‑based cycling
        phase = time.time() % window
        response_data = {
            "pid": pid,
            "uuid": uuid,
            "type": "response",
            'url': url,
            'domain': domain,
            'server_start_ts': server_start_ts,
            'timestamp': datetime.now(timezone.utc),
        }

        if phase < up_ratio * window:
            code = random_successful_code()
            response_data = response_data | {
                'status': 'success', 'message': 'OK', 'code': code}
        else:
            code = random_error_code()
            response_data = response_data | {
                'status': 'error', 'message': 'FAIL', 'code': code}
        http_metrics.insert_response(response_data)
        return response_data, code
