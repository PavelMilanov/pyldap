import json
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
from ldap3.core.exceptions import LDAPAttributeError, LDAPKeyError, LDAPBindError
from .import env, cache
from typing import List, Dict, Final
from models.ldap import (
    OrganizationLdap,
    ResponseLdap,
    CustomerLdap,
    ComputerLdap,
    CustomerLdapDescribe
    )
from pydantic import ValidationError
from loguru import logger


class Ldap3Connector:
    """Основной класс для взаимодействия с AD по протоколу LDAP."""
    _SERVER: Final = Server(env('DC'), get_info=ALL)
    _LOGIN: Final = env('LOGIN')
    _PASSWORD: Final = env('PASSWORD')
    _OU: Final = env.list("DN")[0]
    _DC1: Final = env.list("DN")[1]
    _DC2: Final = env.list("DN")[2]
    
    def __init__(self):
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                logger.info(dc)
        except Exception as e:
            logger.error(e)

    async def get_domain_users(self) -> List[CustomerLdap]:
        """Возвращает список pydantic-моделей всех пользователей в контейнере AD.

        Returns:
            List[CustomerLdap] | None: {
                name=str,
                last_logon=datetime,
                bad_password_time=datetime,
                member_of=list(str),
            }
        """        
        with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
            dc.search(search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_filter='(objectClass=person)', attributes=[ALL_ATTRIBUTES])
            data = [json.loads(unit.entry_to_json()) for unit in dc.entries]
            sorted_data = sorted(data, key=lambda x: x['attributes']['name'][0])  # сортировка по порядку
            users = []
            for user in sorted_data:
                # print(user)
                name=str(user['attributes']['name'][0])
                description = ''  # этого атрибута может не быть, по умолчанию задаем строку
                try:
                    description=str(user['attributes']['description'][0])
                    last_logon=str(user['attributes']['lastLogon'][0])
                    member_of=list(user['attributes']['memberOf'])
                except KeyError:  # пользователь состоит только в группе domain user
                    last_logon=None
                    member_of=None
                users.append(CustomerLdap(
                    name=name,
                    description=description,
                    last_logon=last_logon,
                    member_of=member_of,
                ))
            return users

    async def get_domain_user(self, name: str) -> CustomerLdap | None:
        """Ищет пользователя в домене и возвращает pydantic-модель.

        Args:
            name (str): Имя пользователя.

        Returns:
            Customer | None: {
                name=str,
                description=str,
                last_logon=datetime,
                member_of=list(str)
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_filter=f'(&(objectClass=person)(cn={name}))', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
                user = json.loads(dc.entries[0].entry_to_json())
                # print(user)
                name=str(user['attributes']['name'][0])
                description = ''  # этого атрибута может не быть, по умолчанию задаем строку
                try:
                    description=str(user['attributes']['description'][0])
                    last_logon=str(user['attributes']['lastLogon'][0])
                    member_of=list(user['attributes']['memberOf'])
                except KeyError:  # пользователь состоит только в группе domain user
                    last_logon=None
                    member_of=None
                return CustomerLdap(
                    name=name,
                    description=description,
                    last_logon=last_logon,
                    member_of=member_of,
                )
        except IndexError as e:  # пользователь не найден
            print(e)
            
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
                return units_tree
        except Exception as e:
            print(e)

    # async def search_organization_by_name(self, name: str) -> OrganizationLdap | None:
    #     """Ищет конейнер организации в AD и возвращает pydantic-модель.

    #     Args:
    #         name (str): Название организации.

    #     Returns:
    #         Organization | None: {
    #             name=str,
    #             created_at=datetime,
    #             changed_at=datetime,
    #             dn=str 
    #         }
    #     """        
    #     try:
    #         with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
    #             dc.search(search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}', search_scope=SUBTREE, search_filter=f'(&(objectClass=organizationalUnit)(name={name}))', attributes=ALL_ATTRIBUTES)
    #             unit = dc.entries[0]
    #             print(unit.entry_to_json())
    #             return Organization(
    #                 name=str(unit['name']),
    #                 created_at=str(unit['whenCreated']),
    #                 changed_at=str(unit['whenChanged']),
    #                 dn=str(unit['distinguishedName'])
    #             )
    #     except Exception as e:
    #         print(e)
    #         return None

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
        return count

    async def get_domain_computer(self, name: str) -> ComputerLdap | None:
        """Возврщает pydantic-модель компьютера в контейнере AD.

        Args:
            name (str): имя компьютера

        Returns:
            ComputerLdap: {
                os=(str),
                os_version=(os_version),
                unit=(unit),
            }
        """
        search = f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}'
        filter_pattern = f'(&(objectClass=computer)(cn={name}))'
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=search, search_filter=filter_pattern, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
                computer = json.loads(dc.entries[0].entry_to_json())
                print(computer)
                os=computer['attributes']['operatingSystem'][0],
                version=str(computer['attributes']['operatingSystemVersion'][0])
                unit=str(computer['attributes']['distinguishedName'][0])
                return ComputerLdap(
                    os=os[0],
                    version_os=version,
                    unit=unit,
                )
        except IndexError as e:  # компьютер не найден
            return None

    def get_computers(self) -> List[str]: 
        search = f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}'
        filter_pattern = '(&(objectClass=computer))'
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
                dc.search(search_base=search, search_filter=filter_pattern)
                dn_items = []
                computers = dc.entries
                for computer in computers:
                    data = json.loads(computer.entry_to_json())  # CN=CUSTOMER0003,OU=_,OU=_,OU=_,DC=_,DC=_
                    # print(computer.entry_dn)
                    # item = computer.entry_dn.split(',')[0][3:].lower()  # CUSTOMER0000
                    item = computer.entry_dn
                    dn_items.append(item)
                    return dn_items
                    # elif mode == 'dn-pooling':
                    #     customer = computer.entry_dn.split(',')[0][3:].lower()
                    #     unit = computer.entry_dn.split(',')[1:-4]  # CN=CUSTOMER0003,OU=_,OU=_
                    #     if len(unit) == 1:
                    #         unit = unit[0][3:]  # unit
                    #         dn[unit] = customer
                    #     elif len(unit) > 1:
                    #         format_unit = ''
                    #         for item in unit:
                    #             format_unit += item[3:] + '-'  # subunit-unit
                    #             dn[format_unit[:-1]] = customer
                            # print(customer, format_unit[:-1])
        except Exception as e:
            print(e)
    
    async def delete_computer(self, name: str) -> ResponseLdap:
        """Удаляет компьютер в контейнере AD.

        Args:
            name (str): Название компьютера.

        Returns:
            ResponseLdap: {
                description=str,
                resp_type=str(delResponse)
            }
        """
        with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:
            dc.delete(dn=f'ou={name},ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}')
            return ResponseLdap(
                description=str(dc.result['description']),
                resp_type=str(dc.result['type'])
            )

    async def get_customer_desctibe(self, name) -> CustomerLdapDescribe:
        """Возвращает общую модель CustomerLdap и ComputerLdap.

        Args:
            name (_type_): имя customer.

        Returns:
            CustomerLdapDescribe: {
                name=str,
                description=str,
                last_logon=datetime,
                member_of=list,
                os=str,
                version_os=str,
                unit=list
            }
        """        
        user = await self.get_domain_user(name)
        computer = await self.get_domain_computer(name)
        if computer is None:
            return CustomerLdapDescribe(
            name=user.name,
            description=user.description,
            last_logon=user.last_logon,
            member_of=user.member_of,
            os='',
            version_os='',
            unit=[''],
            ip=''
        )
        ip = cache.get_value(name)
        return CustomerLdapDescribe(
            name=user.name,
            description=user.description,
            last_logon=user.last_logon,
            member_of=user.member_of,
            os=computer.os,
            version_os=computer.version_os,
            unit=computer.unit,
            ip=ip
        )
    
    async def ldap_authentificate(self, name, password) -> bool:
        """Ldap-аутентификация администратора домена.

        Args:
            name (_type_): логин.
            password (_type_): пароль.

        Raises:
            LDAPBindError: неверный пользователь.

        Returns:
            bool: успешная аутентификация.
        """        
        search_tree = f'cn=Users,dc={self._DC1},dc={self._DC2}'
        search_filter = f'(&(objectClass=person)(cn={name}))'
        try:
            with Connection(self._SERVER, user=f'{self._DC1}.{self._DC2}\{name.lower()}', password=password, authentication=NTLM) as dc:
                dc.search(search_base=search_tree, search_filter=search_filter, attributes=['name'])
                user = json.loads(dc.entries[0].entry_to_json())
                if user['attributes']['name'][0].lower() == name.lower():  # проверка на ввод данных администратора домена
                    return True
                # raise LDAPBindError('Вход только для администратора домена')
        except LDAPBindError:
            return False


domain = Ldap3Connector()
