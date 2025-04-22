import random
import string


def get_uuid(length):
    """Generates a random string of specified length.

    Args:
      length: An integer representing the desired length of the string.

    Returns:
      A string of random characters.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
