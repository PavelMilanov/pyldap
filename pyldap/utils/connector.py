from ldap3 import (
    Server,
    Connection,
    ALL,
    NTLM,
    Tls,
    ALL_ATTRIBUTES,
    ALL_OPERATIONAL_ATTRIBUTES,
    LEVEL,
    SUBTREE,
    MODIFY_REPLACE
    )
from ldap3.core.exceptions import LDAPAttributeError, LDAPKeyError
from environs import Env
import json
import ssl
from typing import List, Dict
from models.ldap import (
    OrganizationLdap,
    ResponseLdap,
    CustomerLdap,
    ComputerLdap,
    ComputerLdapOS
    )
from pydantic import ValidationError
from models.schema import ComputerAttributes


env = Env()
env.read_env()


class Ldap3Connector:
    # _SERVER = Server(env('DC'), port=636, use_ssl=True, tls=Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2), get_info=ALL)
    _SERVER = Server(env('DC'), get_info=ALL)
    _LOGIN = env('LOGIN')
    _PASSWORD = env('PASSWORD')
    _OU = env.list("DN")[0]
    _DC1 = env.list("DN")[1]
    _DC2 = env.list("DN")[2]
    
    def __init__(self):
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                print(dc)
        except Exception as e:
            print(e)

    async def get_domain_users(self) -> List[CustomerLdap] | None:
        """Возвращает список pydantic-моделей всех пользователей в контейнере AD.

        Returns:
            List[CustomerLdap] | None: {
                name=str,
                last_logon=datetime,
                bad_password_time=datetime,
                member_of=list(str),
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_filter='(objectClass=person)', attributes=ALL_ATTRIBUTES)
                data = [json.loads(unit.entry_to_json()) for unit in dc.entries]
                users = []
                for user in data:
                    name=str(user['attributes']['name'][0])
                    try:
                        last_logon=str(user['attributes']['lastLogon'][0])
                        bad_password_time=str(user['attributes']['badPasswordTime'][0])
                        member_of=list(user['attributes']['memberOf'])
                    except KeyError as e:  # пользователь состоит только в группе domain user
                        last_logon=None
                        bad_password_time=None
                        member_of=None
                    users.append(CustomerLdap(
                        name=name,
                        last_logon=last_logon,
                        bad_password_time=bad_password_time,
                        member_of=member_of,
                    ))
                return users
        except Exception as e:
            print(e)
            return None

    async def get_domain_user(self, name: str) -> CustomerLdap | None:
        """Ищет пользователя в домене и возвращает pydantic-модель.

        Args:
            name (str): Имя пользователя.

        Returns:
            Customer | None: {
                name=str,
                last_logon=datetime,
                bad_password_time=datetime,
                member_of=list(str)
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_filter=f'(&(objectClass=person)(cn={name}))', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
                user = json.loads(dc.entries[0].entry_to_json())
                print(user)
                name=str(user['attributes']['name'][0])
                try:
                    last_logon=str(user['attributes']['lastLogon'][0])
                    bad_password_time=str(user['attributes']['badPasswordTime'][0])
                    member_of=list(user['attributes']['memberOf'])
                except KeyError:  # пользователь состоит только в группе domain user
                    last_logon=None
                    bad_password_time=None
                    member_of=None    
                return CustomerLdap(
                    name=name,
                    last_logon=last_logon,
                    bad_password_time=bad_password_time,
                    member_of=member_of,
                )
        except IndexError as e:  # пользователь не найден
            return None
            
    async def get_count_users(self) -> int:
        """Возвращает суммарное количество пользователей в контейнере AD.

        Returns:
            int: count.
        """        
        users = await self.get_domain_users()
        return len(users)
    
    async def delete_user(self, name: str)-> ResponseLdap:
        """Удаляет пользователя в контейнере AD.

        Args:
            name (str): имя пользователя.

        Returns:
            ResponseLdap: {
                description=str,
                resp_type=str(addResponse)
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.delete(dn=f'cn={name.lower()},ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}')
                print(dc.result)
                return ResponseLdap(
                    description=str(dc.result['description']),
                    resp_type=str(dc.result['type'])
                )
        except Exception as e:
            print(e)

    async def search_organizations_schema(self) -> Dict | None:
        """Возвращает все подразделения в контейнере домена.

        Returns:
            Dict | None: json-всех подраздлений со всеми атрибутами | None.
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_scope=SUBTREE, search_filter='(objectClass=organizationalUnit)', attributes=ALL_ATTRIBUTES)
                units = [json.loads(unit.entry_to_json()) for unit in dc.entries]
                return units
        except Exception as e:
            print(e)
            return None

    async def search_organizations_tree(self) -> Dict[str, List[str]] | None:
        """Возвращает все подраздления со вложенностью ввиде словаря.

        Returns:
            Dict[str, List[str]] | None: {'Temp': ['Unit1', 'Unit2']} | None.
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_scope=LEVEL, search_filter='(objectClass=organizationalUnit)', attributes=['name'])
                units_tree = dict()
                for unit in dc.entries:
                    data = json.loads(unit.entry_to_json())
                    tree_item = data['attributes']['name'][0]
                    dc.search(search_base=f'ou={tree_item},ou=ARMs,ou={env.list("DN")[0]},dc={env.list("DN")[1]},dc={env.list("DN")[2]}', search_scope=LEVEL, search_filter='(objectClass=organizationalUnit)', attributes=['name'])
                    if len(dc.entries) > 0:  # если есть вложенность
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

    async def search_organization_by_name(self, name: str) -> OrganizationLdap | None:
        """Ищет конейнер организации в AD и возвращает pydantic-модель.

        Args:
            name (str): Название организации.

        Returns:
            Organization | None: {
                name=str,
                created_at=datetime,
                changed_at=datetime,
                dn=str 
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_scope=SUBTREE, search_filter=f'(&(objectClass=organizationalUnit)(name={name}))', attributes=ALL_ATTRIBUTES)
                unit = dc.entries[0]
                print(unit.entry_to_json())
                return Organization(
                    name=str(unit['name']),
                    created_at=str(unit['whenCreated']),
                    changed_at=str(unit['whenChanged']),
                    dn=str(unit['distinguishedName'])
                )
        except Exception as e:
            print(e)
            return None

    async def get_count_organizations(self) -> int:
        """Возвращает число подразделений в контейнере AD.

        Returns:
            int: count.
        """        
        organizations = await self.search_organizations_tree()
        count = 0
        for unit, subunit in organizations.items():
            count += 1
            if len(subunit) > 1:  # если подраздление имет вложенность
                for org in subunit:
                    count += 1
        print(count)
        return count
                    
    async def add_organization(self, name: str) -> ResponseLdap:
        """Создает подразделение в контейнере AD.

        Args:
            name (str): Название подраздленения.

        Returns:
            ResponseLdap: {
                description=str,
                resp_type=str(addResponse)
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.add(dn=f'ou={name},ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', object_class=['organizationalUnit', 'top'], attributes=None)
                print(dc.result)
                return ResponseLdap(
                    description=str(dc.result['description']),
                    resp_type=str(dc.result['type'])
                )
        except Exception as e:
            print(e)

    async def delete_organization(self, name: str) -> ResponseLdap:
        """Удаляет подразделение в контейнере AD.

        Args:
            name (str): Название подраздленения.

        Returns:
            ResponseLdap: {
                description=str,
                resp_type=str(delResponse)
            }
        """
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.delete(dn=f'ou={name},ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}')
                print(dc.result)
                return ResponseLdap(
                    description=str(dc.result['description']),
                    resp_type=str(dc.result['type'])
                )
        except Exception as e:
            print(e)
    
    async def get_computer(self, attribute: str, name: str = None, attribute_value: str = None) -> List[ComputerLdap]:
        """Возврщает pydantic-модель компьютера в контейнере AD.

        Args:
            name (str): имя компьютера

        Returns:
            ComputerLdap: {
                name=(str),
                os=(str),
                os_version=(os_version),
                unit=(unit),
            }
        """
        search = f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}'
        match attribute:
            case 'cn':  # поиск по имени компьютера
                filter_pattern = f'(&(objectClass=computer)({attribute}={name}))'
                with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                    dc.search(search_base=search, search_filter=filter_pattern, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
                    computer = json.loads(dc.entries[0].entry_to_json())
                    print(computer['dn'])
                    name=str(computer['attributes']['name'][0])
                    os=ComputerLdapOS(
                        name=str(computer['attributes']['operatingSystem'][0]),
                        version=str(computer['attributes']['operatingSystemVersion'][0])
                    )
                    unit=str(computer['attributes']['distinguishedName'][0])
                    return [ComputerLdap(
                        name=name,
                        os=os,
                        unit=unit,
                    )]
            case 'operatingSystem':  # поиск по названию операционной системе
                if attribute_value is None:
                    raise ValueError(f'Не указан аргумент для {attribute}')
                print(attribute_value)
                filter_pattern = f'(&(objectClass=computer)({attribute}=*))'
                with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                    dc.search(search_base=search, search_filter=filter_pattern, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
                    computers = []
                    for computer in dc.entries:
                        data = json.loads(computer.entry_to_json())
                        print(data)
                        if str(data['attributes']['operatingSystem'][0].lower()).find(attribute_value.lower()) != -1:  # Если найдено совпадение (Windows 7 Профессиональня == Windows 7)
                            name=str(data['attributes']['name'][0])
                            os=ComputerLdapOS(
                                name=str(data['attributes']['operatingSystem'][0]),
                                version=str(data['attributes']['operatingSystemVersion'][0])
                            )   
                            unit=str(data['attributes']['distinguishedName'][0])
                            computers.append(ComputerLdap(
                                name=name,
                                os=os,
                                unit=unit,
                            ))
                    return computers
            case 'dn':
                print(attribute)
                if attribute_value is None:
                    raise ValueError(f'Не указан аргумент для {attribute}')
                filter_pattern = f'(&(objectClass=computer)({attribute}={attribute_value}))'
                with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                    dc.search(search_base=search, search_filter=filter_pattern, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
                    computer = json.loads(dc.entries[0].entry_to_json())
                    print(computer['dn'])
                    name=str(computer['attributes']['name'][0])
                    os=ComputerLdapOS(
                        name=str(computer['attributes']['operatingSystem'][0]),
                        version=str(computer['attributes']['operatingSystemVersion'][0])
                    )
                    unit=str(computer['attributes']['distinguishedName'][0])
                    return [ComputerLdap(
                        name=name,
                        os=os,
                        unit=unit,
                    )]
            case _:
                raise ValueError(f'Не указаны аргументы для поиска')
    
    
domain = Ldap3Connector()