import redis


def get_client():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r