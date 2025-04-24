import requests
from typing import Dict, Optional, Union, Any
import json
import logging
import time

logging.basicConfig(level=logging.DEBUG, force=True)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def is_up(*, url: str, method: str = 'GET', body: Optional[Union[str, Dict[str, Any]]] = None,
         headers: Optional[Dict[str, str]] = None) -> int:
    """
    Pings the specified URL with the given method, body, and headers.

    :param url: The URL to ping.
    :param method: The HTTP method to use (default is 'GET').
    :param body: The body of the request (default is None).
    :param headers: The headers for the request (default is None).
    :return: The HTTP status code from the server.
    :raises: requests.exceptions.RequestException if the request fails
    """
    if headers is None:
        headers = {}
    
    if body is not None and 'Content-Type' not in headers and 'content-type' not in headers:
        headers['Content-Type'] = 'application/json'
    
    if isinstance(body, dict):
        body = json.dumps(body)
    
    start_time = time.time()
    try:
        response = requests.request(
            method=method,
            url=url,
            data=body,
            headers=headers,
            timeout=5  # 5 second timeout
        )
    except requests.Timeout as err:
        logger.error({"url": url, "status_code": -1, "available": 0, "error": str(err)})
        return False
    except requests.exceptions.ConnectionError as err:
        logger.error({"url": url, "status_code": -1, "available": 0, "error": str(err)})
        return False

    elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
    if elapsed > 500:
        logger.error({"url": url, "status_code": response.status_code, "available": 0, "elapsedMs": elapsed, "message": f"{url} took too long to respond: {elapsed}ms"})
        return False
    
    if response.status_code < 200 or response.status_code > 299:
        logger.debug({"url": url, "status_code": response.status_code, "available": 0, "elapsedMs": elapsed})
        return False
    else:
        logger.debug({"url": url, "status_code": response.status_code, "available": 1, "elapsedMs": elapsed})
        return True
