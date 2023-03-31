import pytest
from pyldap.utils.connector import Ldap3Connector

server = Ldap3Connector()

def test_search_users():
    server.search_domain_users()
