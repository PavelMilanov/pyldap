#  внешние пакеты
from environs import Env
#  внутренние пакеты
from .redis import RedisConnector


env = Env()
env.read_env()


__all__ = ['RedisConnector']
