from hashlib import md5

from ninja.security import APIKeyHeader

from django.core.exceptions import ObjectDoesNotExist

from .models import User

AUTH_KEY = "token"


class ApiKey(APIKeyHeader):
    """Class to provide authentication via token in header."""

    param_name = AUTH_KEY

    def authenticate(self, request, token):
        """
        Parse token submission and check validity.

        Tokens are formatted like:
            "<username>:<hash>"

        On success, returns username.

        On failure, returns None. Error message JSON is automatically generated:
            {"detail": "Unauthorized"}
        """
        print("in authenticate")

        if not check_token(token):
            return None

        username = token.split(":")[0]

        try:
            user = User.objects.get(username=username)

        except ObjectDoesNotExist:
            return None

        return user


token_header = ApiKey()


# Author's note: these auth functions are for didactic purposes only. Never do
# this in real life!

def generate_token(username):
    """
    Generate an auth token by hashing username and concatenating username
    with truncated version of hash.

    EX: "fluffy" -> "fluffy:ce7bcda695c3"
    """
    print("in generate_token")

    hash = generate_hash(username)

    return f"{username}:{hash}"


def generate_hash(username):
    """
    Hash username and return first 12 characters.

    EX: "fluffy" -> "ce7bcda695c3"
    """
    print("in generate_hash")

    encoded_username = username.encode()
    h = md5()
    h.update(encoded_username)
    hashed_username = h.hexdigest()

    # STAFFNOTE: We are reducing the size of the hash for readability for the
    # students. PLEASE NEVER REALLY DO THIS
    truncated_hash = hashed_username[0:12]
    print("truncated hash:", truncated_hash)

    return truncated_hash


def check_token(token):
    """
    Re-hash username and check against user-submitted token.

    Returns a boolean.
    """
    print("in check_token")

    try:
        username, hash = token.split(":")
    # A malformed username will raise a ValueError
    # A missing header will raise an AttributeError
    except (ValueError, AttributeError):
        return False

    return generate_hash(username) == hash
