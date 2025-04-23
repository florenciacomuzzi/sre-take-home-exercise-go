def clean_url(url: str) -> str:
    """
    Cleans the URL by removing the trailing slash if it exists.

    :param url: The URL to clean.
    :return: The cleaned URL.
    """
    if url.endswith('/'):
        return url[:-1]
    return url