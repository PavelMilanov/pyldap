from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, LEVEL, SUBTREE
from environs import Env
import json
from typing import List, Dict


env = Env()
env.read_env()

class Ldap3Connector:
    
    _SERVER = Server(env('DC'), get_info=ALL)
    _LOGIN = env('LOGIN')
    _PASSWORD = env('PASSWORD')
    _OU = env.list("DN")[0]
    _DC1 = env.list("DN")[1]
    _DC2 = env.list("DN")[2]
    

    def search_domain_users(self):
       with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
            dc.search(search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_filter='(objectCategory= person)', attributes=ALL_ATTRIBUTES)
            data = dc.entries
            print(data)

    async def search_organizations_schema(self) -> Dict | None:
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_scope=SUBTREE, search_filter='(objectCategory=organizationalUnit)', attributes=ALL_ATTRIBUTES)
                units = [json.loads(unit.entry_to_json()) for unit in dc.entries]
                return units
        except Exception as e:
            print(e)
            return None
    
    async def search_organizations_tree(self) -> Dict[str, List[str]] | None:
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_scope=LEVEL, search_filter='(objectCategory=organizationalUnit)', attributes=['name'])
                units_tree = dict()
                for unit in dc.entries:
                    data = json.loads(unit.entry_to_json())
                    tree_item = data['attributes']['name'][0]
                    dc.search(search_base=f'ou={tree_item},ou=ARMs,ou={env.list("DN")[0]},dc={env.list("DN")[1]},dc={env.list("DN")[2]}', search_scope=LEVEL, search_filter='(objectCategory=organizationalUnit)', attributes=['name'])
                    if len(dc.entries) > 0:
                        tree_subitems = []
                        for subunit in dc.entries:
                            data = json.loads(subunit.entry_to_json())
                            tree_subitems.append(str(data['attributes']['name'][0]))
                        units_tree[str(tree_item)] = tree_subitems
                    else:
                        units_tree[str(tree_item)] = []
                print(units_tree)
                return units_tree
        except Exception as e:
            print(e)
            return None


domain = Ldap3Connector()