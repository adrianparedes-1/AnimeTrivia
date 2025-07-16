import redis


def get_client():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r


def delete_keys_containing(user_id):
    """
    Delete all keys in Redis containing the given substring.
    """
    r = get_client()
    keys = r.keys(f"{user_id}:*")
    if keys:
        r.delete(*keys)
