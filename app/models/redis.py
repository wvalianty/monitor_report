import redis
from flask import current_app


class REDIS:
    def __init__(self):
        redis_conf = current_app.config["REDIS"]
        pool = redis.ConnectionPool(host=redis_conf.get("host"), port=redis_conf.get("port"), db=redis_conf.get("db"),password=redis_conf.get("password"))
        self.r = redis.Redis(connection_pool=pool)

    def rset(self,key, value, ex):
        status = self.r.set(key, value, ex=ex, nx=True)
        if status:
            return True
        else:
            return False

    def rdel(self,key):
        status = self.r.delete(key)
        if status:
            return True
        else:
            return False

    def is_exist(self,key):
        status = self.r.get(key)
        if status:
            return True
        else:
            return False