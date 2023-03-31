from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, LEVEL, SUBTREE
from environs import Env
import json

env = Env()
env.read_env()

server = Server(env('DC'), get_info=ALL)

try:
    with Connection(server, user=env('LOGIN'), password=env('PASSWORD') , authentication=NTLM) as dc:
        dc.search(search_base=f'ou=ARMs,ou={env.list("DN")[0]},dc={env.list("DN")[1]},dc={env.list("DN")[2]}', search_scope=LEVEL, search_filter='(objectCategory=organizationalUnit)', attributes=ALL_ATTRIBUTES)
        # data = dc.entries[0].entry_to_json()
        for unit in dc.entries:
            data = json.loads(unit.entry_to_json())
            print(type(data))
            # print(data['name'])    
except Exception as e:
    print(e)
finally:
    pass
   