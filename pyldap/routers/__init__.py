#  внешние пакеты
from environs import Env
from utils import Ldap3Connector

ldap = Ldap3Connector()
env = Env()
env.read_env()