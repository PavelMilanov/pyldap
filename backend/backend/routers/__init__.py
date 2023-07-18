#  внешние пакеты
from environs import Env
from utils import Ldap3Connector
from db.redis import RedisConnector


ldap = Ldap3Connector()
cache = RedisConnector()

env = Env()
env.read_env()
