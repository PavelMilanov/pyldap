import redis
from typing import Set, List, Final
from loguru import logger

from .import env


class RedisConnector:
    
    _IP: Final = (env('REDIS_HOST'))
    _PORT: Final = 6379
    CONN = redis.Redis(host=_IP, port=_PORT, decode_responses=True)


    def set_value(self, key: str, value: str) -> None:
        """Redis SET command.

        Args:
            key (str): key.
            value (str): value.
        """
        try:     
            self.CONN.set(key, value)
        except Exception as e:
            logger.exception(e)

    def get_value(self, key: str) -> str:
        """Redis GET command.

        Args:
            key (str): key.

        Returns:
            str: value.
        """        
        try:
            data = self.CONN.get(key)
            return data.decode('utf-8')
        except AttributeError as e:
            return data

    def delete_value(self, key: str) -> None:
        """Redis DEL command.

        Args:
            key (str): key.
        """        
        try:
            self.CONN.delete(key)
        except Exception as e:
            logger.exception(e)

    def add_set_item(self, set_name: str, set_value: str) -> None:
        """Redis SADD command.

        Args:
            set_name (str): key.
            set_value (str): value.
        """
        try:
            self.CONN.sadd(set_name, set_value)
        except Exception as e:
            logger.exception(e)

    def get_set_items(self, set_name: str) -> Set[str]:
        """Redis SINTER command.

        Args:
            set_name (str): key.

        Returns:
            _Set[str]: unit's set.
        """
        try:
            return self.CONN.sinter(set_name)
        except Exception as e:
            logger.exception(e)

    def delete_set_items(self, set_name: str, set_value: str) -> None:
        """Redis SREM command.

        Args:
            set_name (str): key.
            set_value (str): value.
        """
        try:        
            self.CONN.srem(set_name, set_value)
        except Exception as e:
            logger.exception(e)

    def set_json_set(self, set_name: str, value: List[dict]) -> int:
        """Redis JSON.SET command.

        Args:
            set_name (str): key.
            value (List[dict]): values.

        Returns:
            int: status.
        """
        try:        
            return self.CONN.json().set(set_name, '$', value)
        except Exception as e:
            logger.exception(e)

    def get_json_set(self, set_name: str, skip: int = None, limit: int = None) -> List[dict]:      
        """Redis JSON.GET command.

        Args:
            set_name (str): key.
            skip (int, optional): first index. 
            limit (int, optional): last index.

        Returns:
            List[dict]: values.
        """
        try:
            if skip is None and limit is None:
                return self.CONN.json().get(set_name, '$')
            elif skip is None and limit is not None:
                return self.CONN.json().get(set_name, f'$[{limit}]')
            return self.CONN.json().get(set_name, f'$[{skip}:{limit}]')
        except Exception as e:
            logger.exception(e)

    def del_json_set(self, set_name: str) -> int:
        """Redis JSON.DEL command.

        Args:
            set_name (str): key.

        Returns:
            int: status.
        """
        try:        
            return self.CONN.json().delete(set_name)
        except Exception as e:
            logger.exception(e)

    def append_json_set(self, set_name: str, data: dict) -> int:
        """Redis JSON.ARRAPPEND command.

        Args:
            set_name (str): key.
            data (dict): values.

        Returns:
            int: status.
        """        
        try:
            return self.CONN.json().arrappend(set_name, '$', data)
        except Exception as e:
            logger.exception(e)

    def clear_json_set(self, set_name: str) -> int:
        """Redis JSON.CLEAR command.

        Args:
            set_name (str): key.

        Returns:
            int: status.
        """       
        try:
            return self.CONN.json().clear(set_name)
        except Exception as e:
            logger.exception(e)
