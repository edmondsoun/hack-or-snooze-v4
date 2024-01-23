from hashlib import md5

from django.core.exceptions import ObjectDoesNotExist

from ninja.security import APIKeyHeader

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

        On success, returns user instance.

        On failure, returns None. Error message JSON is automatically generated:
            {"detail": "Unauthorized"}
        """

        if not check_token(token):
            return None

        username = token.split(":")[0]

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

        return user


# Instantiate token_header to use in API routes:
token_header = ApiKey()


###############################################################################
# Helper functions to generate and validate tokens

# Author's note: these auth functions are for didactic purposes only. Never do
# this in real life!

def generate_token(username):
    """
    Generate an auth token by hashing username and concatenating username
    with truncated version of hash.

    EX: "fluffy" -> "fluffy:ce7bcda695c3"
    """

    hash = generate_hash(username)

    return f"{username}:{hash}"


def generate_hash(username):
    """
    Hash username and return first 12 characters.

    EX: "fluffy" -> "ce7bcda695c3"
    """

    encoded_username = username.encode()
    h = md5()
    h.update(encoded_username)
    hashed_username = h.hexdigest()

    # We are reducing the size of the hash for readability for the students.
    # PLEASE NEVER REALLY DO THIS!
    truncated_hash = hashed_username[0:12]

    return truncated_hash


def check_token(token):
    """
    Re-hash username and check against user-submitted token.

    Returns a boolean.

    EX:
    "fluffy:ce7bcda695c3" -> True
    "bad::token" -> False
    no header (token == None) -> False
    """

    try:
        username, hash = token.split(":")
    # A malformed token will raise a ValueError
    # A missing header will raise an AttributeError
    except (ValueError, AttributeError):
        return False

    return generate_hash(username) == hash
