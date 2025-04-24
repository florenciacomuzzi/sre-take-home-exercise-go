import random
import string
from urllib.parse import urlparse


def get_uuid(length):
    """Generates a random string of specified length.

    Args:
      length: An integer representing the desired length of the string.

    Returns:
      A string of random characters.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_domain(url):
    """
    Extract the domain from a URL.

    :param url: The URL to extract the domain from
    :return: The domain as a string
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split(':')[0]  # Remove port number if present
    return domain

def clean_url(url: str) -> str:
    """
    Cleans the URL by removing the trailing slash if it exists.

    :param url: The URL to clean.
    :return: The cleaned URL.
    """
    if url.endswith('/'):
        return url[:-1]
    return url