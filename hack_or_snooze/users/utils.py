from hashlib import md5

# Author's note: this approach to auth is for didactic purposes only. Never do
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
    # TODO: check if we can limit digest without manually truncating?
    hashed_username = h.hexdigest()

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
    except ValueError:
        return False

    return generate_hash(username) == hash

