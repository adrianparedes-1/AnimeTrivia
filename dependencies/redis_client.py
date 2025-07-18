import redis


def get_client():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r


def delete_keys_containing(user_id):
    """
    Delete all keys in Redis containing the given substring.
    """
    cursor = 0
    r = get_client()
    while True:
        cursor, keys = r.scan(cursor=cursor, match=f"{user_id}*", count=1000)
        if keys:
            r.delete(*keys)
            print(f"Deleted keys: {keys}")
        if cursor == 0:
            break