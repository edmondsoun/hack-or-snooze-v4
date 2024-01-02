from .utils import check_token
from ninja.security import APIKeyHeader
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

        if check_token(token):
            username = token.split(":")[0]
            return username
