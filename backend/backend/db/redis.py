import redis
from .import env
from typing import Set, List


class RedisConnector:

    def __init__(self, ip: str = 'localhost', port: int = 6379):
        self.connect = redis.Redis(host=ip, port=port, decode_responses=True)

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
            return data

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

    def set_json_set(self, set_name: str, value: List[dict]) -> int:
        """Redis JSON.SET command.

        Args:
            set_name (str): key.
            value (List[dict]): values.

        Returns:
            int: status.
        """        
        return self.connect.json().set(set_name, '$', value)
    
    def get_json_set(self, set_name: str, skip: int, limit: int) -> List[dict]:
        """Redis JSON.GET command.

        Args:
            set_name (str): key.
            skip (int): first index. 
            limit (int): last index.

        Returns:
            List[dict]: values.
        """        
        return self.connect.json().get(set_name, f'$[{skip}:{limit}]')
    
    def del_json_set(self, set_name: str) -> int:
        """Redis JSON.DEL command.

        Args:
            set_name (str): key.

        Returns:
            int: status.
        """        
        return self.connect.json().delete(set_name)