from hashlib import md5


def check_token(username, token):
    """Helper function to re-hash username and check against
    user-submitted token."""

    encoded_username = username.encode()
    h = md5()
    h.update(encoded_username)
    hashed_username = h.hexdigest()

    truncated_hash = hashed_username[0:12]

    print("DEBUGGING HASH CHECK", truncated_hash)
    return truncated_hash == token