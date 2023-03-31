from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, LEVEL, SUBTREE
from environs import Env
import json

env = Env()
env.read_env()

server = Server(env('DC'), get_info=ALL)

try:
    with Connection(server, user=env('LOGIN'), password=env('PASSWORD') , authentication=NTLM) as dc:
        dc.search(search_base=f'ou=ARMs,ou={env.list("DN")[0]},dc={env.list("DN")[1]},dc={env.list("DN")[2]}', search_scope=LEVEL, search_filter='(objectCategory=organizationalUnit)', attributes=['name'])
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
except Exception as e:
    print(e)
finally:
    pass
   