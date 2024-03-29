import json
from ldap3.core.exceptions import LDAPBindError
from loguru import logger
from typing import List, Dict, Final
from ldap3 import (
    Server,
    Connection,
    ALL,
    NTLM,
    ALL_ATTRIBUTES,
    ALL_OPERATIONAL_ATTRIBUTES,
    LEVEL,
    SUBTREE,
    )

from .import env
from models.ldap import (
    CustomerLdap,
    ComputerLdap,
    CustomerLdapDescribe
    )


class Ldap3Connector:
    """Основной класс для взаимодействия с AD по протоколу LDAP."""
    _SERVER: Final = Server(env('DC'), get_info=ALL)
    _LOGIN: Final = env('LOGIN')
    _PASSWORD: Final = env('PASSWORD')
    _OU: Final = env.list("DN")[0]
    _DC1: Final = env.list("DN")[1]
    _DC2: Final = env.list("DN")[2]
    
    def get_domain_users(self, skip: int = None, limit: int = None) -> List[CustomerLdap]:  # noqa: E501
        """Возвращает список pydantic-моделей всех пользователей в контейнере AD.
        
        Args:
            skip (int, optional): Начальный индекс списка пользователей. Defaults to None.
            limit (int, optional): Конечный индекс списка пользователей. Defaults to None.
            
        Returns:
            List[CustomerLdap] | None: {
                name=str,
                bad_password_time=datetime,
                member_of=list(str),
            }
        """        
        with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:  # noqa: E501
            dc.search(
                search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}',
                search_filter='(objectClass=person)',
                attributes=[ALL_ATTRIBUTES]
                )
            data = [json.loads(unit.entry_to_json()) for unit in dc.entries]
            # сортировка по порядку
            sorted_data = sorted(data, key=lambda x: x['attributes']['name'][0])
            users = []
            for user in sorted_data[skip:limit]:
                name=str(user['attributes']['name'][0])
                # этого атрибута может не быть, по умолчанию задаем строку
                description = ''
                try:
                    description=str(user['attributes']['description'][0])
                    member_of=list(user['attributes']['memberOf'])
                except KeyError:  # пользователь состоит только в группе domain user
                    # last_logon=None
                    member_of=None
                users.append(CustomerLdap(
                    name=name,
                    description=description,
                    member_of=member_of,
                ))
            return users

    def get_domain_user(self, name: str) -> CustomerLdap | None:
        """Ищет пользователя в домене и возвращает pydantic-модель.

        Args:
            name (str): Имя пользователя.

        Returns:
            Customer | None: {
                name=str,
                description=str,
                member_of=list(str)
            }
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:  # noqa: E501
                dc.search(
                    search_base=f'ou=Customer,ou=Customers,ou={self._OU},dc={self._DC1},dc={self._DC2}',
                    search_filter=f'(&(objectClass=person)(cn={name}))',
                    attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES]
                    )
                user = json.loads(dc.entries[0].entry_to_json())
                name=str(user['attributes']['name'][0])
                # этого атрибута может не быть, по умолчанию задаем строку
                description = ''
                try:
                    description=str(user['attributes']['description'][0])
                    member_of=list(user['attributes']['memberOf'])
                except KeyError:  # пользователь состоит только в группе domain user
                    member_of=None
                return CustomerLdap(
                    name=name,
                    description=description,
                    member_of=member_of,
                )
        except IndexError as e:  # пользователь не найден
            logger.error(e)
    
    def search_organizations_schema(self) -> Dict | None:
        """Возвращает все подразделения в контейнере домена.

        Returns:
            Dict | None: json-всех подраздлений со всеми атрибутами | None.
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:  # noqa: E501
                dc.search(
                    search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}',
                    search_scope=SUBTREE, search_filter='(objectClass=organizationalUnit)',  # noqa: E501
                    attributes=ALL_ATTRIBUTES
                    )
                units = [json.loads(unit.entry_to_json()) for unit in dc.entries]
                return units
        except Exception as e:
            logger.exception(e)
            return None

    def search_organizations_tree(self) -> Dict[str, List[str]] | None:
        """Возвращает все подраздления со вложенностью ввиде словаря.

        Returns:
            Dict[str, List[str]] | None: {'Temp': ['Unit1', 'Unit2']} | None.
        """        
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:  # noqa: E501
                dc.search(
                    search_base=f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}',
                    search_scope=LEVEL, search_filter='(objectClass=organizationalUnit)',
                    attributes=['name']
                    )
                units_tree = dict()
                for unit in dc.entries:
                    data = json.loads(unit.entry_to_json())
                    tree_item = data['attributes']['name'][0]
                    dc.search(
                        search_base=f'ou={tree_item},ou=ARMs,ou={env.list("DN")[0]},dc={env.list("DN")[1]},dc={env.list("DN")[2]}',
                        search_scope=LEVEL, search_filter='(objectClass=organizationalUnit)',  # noqa: E501
                        attributes=['name']
                        )
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
            logger.exception(e)

    def get_count_organizations(self) -> int:
        """Возвращает число подразделений в контейнере AD.

        Returns:
            int: count.
        """        
        organizations = self.search_organizations_tree()
        count = 0
        for unit, subunit in organizations.items():
            count += 1
            if len(subunit) > 1:  # если подраздление имет вложенность
                for org in subunit:
                    count += 1
        return count

    def get_domain_computer(self, name: str) -> ComputerLdap | None:
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
        os = ''
        version = ''
        unit = ''
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:  # noqa: E501
                dc.search(
                    search_base=search,
                    search_filter=filter_pattern,
                    attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES]
                    )
                computer = json.loads(dc.entries[0].entry_to_json())
                os=computer['attributes']['operatingSystem'][0]
                version=str(computer['attributes']['operatingSystemVersion'][0])
                unit=str(computer['attributes']['distinguishedName'][0])
        except IndexError:  # компьютер не найден
            logger.error(f'компьютер {name} не найден в лесу')
        except KeyError:
            pass
        return ComputerLdap(
                    os=os,
                    version_os=version,
                    unit=unit,
                )

    def get_customer_desctibe(self, name: str) -> CustomerLdapDescribe:
        """Возвращает общую модель CustomerLdap и ComputerLdap.

        Args:
            name (str): имя customer.

        Returns:
            CustomerLdapDescribe: {
                name=str,
                description=str,
                member_of=list,
                os=str,
                version_os=str,
                unit=list
            }
        """        
        user = self.get_domain_user(name)
        computer = self.get_domain_computer(name)
        if computer is None:
            return CustomerLdapDescribe(
            name=user.name,
            description=user.description,
            member_of=user.member_of,
            os='',
            version_os='',
            unit=[''],
        )
        return CustomerLdapDescribe(
            name=user.name,
            description=user.description,
            member_of=user.member_of,
            os=computer.os,
            version_os=computer.version_os,
            unit=computer.unit,
        )
    
    def get_computers(self) -> List[str]:
        """Поиск всех компьюентров.
        Требуется для задачи по рассписанию.

        Returns:
            List[str]:
        """        
        search = f'ou=ARMs,ou={self._OU},dc={self._DC1},dc={self._DC2}'
        filter_pattern = '(&(objectClass=computer))'
        try:
            with Connection(self._SERVER, user=self._LOGIN, password=self._PASSWORD, authentication=NTLM) as dc:  # noqa: E501
                dc.search(search_base=search, search_filter=filter_pattern)
                dn_items = []
                computers = dc.entries
                for computer in computers:
                    # CN=CUSTOMER0003,OU=_,OU=_,OU=_,DC=_,DC=
                    # data = json.loads(computer.entry_to_json())
                    item = computer.entry_dn
                    dn_items.append(item)
                return dn_items
        except Exception as e:
            logger.exception(e)

    def ldap_authentificate(self, name: str, password: str) -> bool:
        """Ldap-аутентификация администратора домена.

        Args:
            name (str): логин.
            password (str): пароль.

        Raises:
            LDAPBindError: неверный пользователь.

        Returns:
            bool: статус.
        """        
        search_tree = f'cn=Users,dc={self._DC1},dc={self._DC2}'
        search_filter = f'(&(objectClass=person)(cn={name}))'
        try:
            with Connection(self._SERVER, user=f'{self._DC1}.{self._DC2}\{name.lower()}', password=password, authentication=NTLM) as dc:  # noqa: E501, E999
                dc.search(
                    search_base=search_tree,
                    search_filter=search_filter,
                    attributes=['name']
                    )
                user = json.loads(dc.entries[0].entry_to_json())
                # проверка на ввод данных администратора домена
                if user['attributes']['name'][0].lower() == name.lower():
                    return True
        except LDAPBindError as e:
            logger.error(e)
            return False
