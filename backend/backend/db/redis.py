import redis
from .import env
from typing import Set


class RedisConnector:
    
    def __init__(self, ip: str = 'redis', port: int = 6379, decode_responses=True):
        self.connect = redis.Redis(host=ip, port=port)

    def set_value(self, key: str, value: str):
        resp = self.connect.set(key, value)
        print(resp)
    
    def get_value(self, key: str) -> str:
        try:
            data = self.connect.get(key)
            return data.decode('utf-8')
        except AttributeError as e:
            return '-'

    def delete_value(self, key: str) -> None:
        self.connect.delete(key)
    
    def add_set_item(self, set_name: str, set_value: str) -> None:
        self.connect.sadd(set_name, set_value)
    
    def get_set_items(self, set_name: str):
        return self.connect.sinter(set_name)

    def delete_set_items(self, set_name: str, set_value: str) -> None:
        self.connect.srem(set_name, set_value)
