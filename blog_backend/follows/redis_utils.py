from django_redis import get_redis_connection

def get_redis():
    return get_redis_connection('default')

def user_following_key(user_id):
    return f'follows:{user_id}'

def add_follow(user_id, followed_id):
    """添加关注关系至 Redis Set"""
    conn = get_redis()
    conn.sadd(user_following_key(user_id), followed_id)

def remove_follow(user_id, followed_id):
    """移除关注关系"""
    conn = get_redis()
    conn.srem(user_following_key(user_id), followed_id)

def get_following_ids(user_id):
    """获取用户关注的所有人 ID 列表"""
    conn = get_redis()
    return [int(uid) for uid in conn.smembers(user_following_key(user_id))]

def is_following(user_id, followed_id):
    """检查是否已关注"""
    conn = get_redis()
    return conn.sismember(user_following_key(user_id), followed_id)