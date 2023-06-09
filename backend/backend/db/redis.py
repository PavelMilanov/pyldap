import redis
from .import env
from typing import Set


class RedisConnector:
    
    def __init__(self, ip: str = 'redis', port: int = 6379, decode_responses=True):
        self.connect = redis.Redis(host=ip, port=port)

    def set_value(self, key: str, value: str) -> None:
        """Redis SET command.

        Args:
            key (str): key.
            value (str): value.
        """        
        self.connect.set(key, value)
    
    def get_value(self, key: str) -> str:
        """Redis GET command.

        Args:
            key (str): key.

        Returns:
            str: value.
        """        
        try:
            data = self.connect.get(key)
            return data.decode('utf-8')
        except AttributeError as e:
            return '-'

    def delete_value(self, key: str) -> None:
        self.connect.delete(key)
    
    def add_set_item(self, set_name: str, set_value: str) -> None:
        """Redis SADD command.

        Args:
            set_name (str): key.
            set_value (str): value.
        """        
        self.connect.sadd(set_name, set_value)
    
    def get_set_items(self, set_name: str) -> Set[str]:
        """Redis SINTER command.

        Args:
            set_name (str): key.

        Returns:
            _Set[str]: unit's set.
        """        
        return self.connect.sinter(set_name)

    def delete_set_items(self, set_name: str, set_value: str) -> None:
        """Redis SREM command.

        Args:
            set_name (str): key.
            set_value (str): value.
        """        
        self.connect.srem(set_name, set_value)
