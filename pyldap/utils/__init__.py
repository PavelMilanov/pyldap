#  внешние пакеты
from environs import Env

env = Env()
env.read_env()

#  внутренние пакеты
from .connector import Ldap3Connector
from .auth import Authentification

__all__ = ['Authentication', 'Ldap3Connector']
