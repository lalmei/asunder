from urllib.parse import urlparse


def is_url(path: str) -> bool:
    """
    Checks if a given path is a URL.

    Args:
        path: The path to check.

    Returns:
        True if the path is a URL, False otherwise.
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
