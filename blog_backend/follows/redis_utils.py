from django_redis import get_redis_connection

def get_redis():
    return get_redis_connection('default')

def user_following_key(user_id):
    return f'follows:{user_id}'

def add_follow(user_id, followed_id):
    conn = get_redis()
    conn.sadd(user_following_key(user_id), followed_id)

def remove_follow(user_id, followed_id):
    conn = get_redis()
    conn.srem(user_following_key(user_id), followed_id)

def get_following_ids(user_id):
    conn = get_redis()
    return [int(uid) for uid in conn.smembers(user_following_key(user_id))]

def is_following(user_id, followed_id):
    conn = get_redis()
    return conn.sismember(user_following_key(user_id), followed_id)