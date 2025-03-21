from django_redis import get_redis_connection


class RedisService:
    __instance = None

    def __init__(self):
        if RedisService.__instance is None:
            self.__redis = get_redis_connection("default")
            RedisService.__instance = self
        else:
            raise Exception("Can't create more than one instances")

    @staticmethod
    def get_instance():
        if RedisService.__instance is None:
            RedisService()
        return RedisService.__instance

    def get(self, key):
        value = self.__redis.get(key)
        if value:
            return value.decode()
        return value

    def set(self, key, value, timeout):
        return self.__redis.set(key, value, timeout)

    def update(self, key, value, timeout=None):
        if self.__redis.exists(key):
            self.__redis.set(key, value, timeout)

    def delete(self, key):
        self.__redis.delete(key)
