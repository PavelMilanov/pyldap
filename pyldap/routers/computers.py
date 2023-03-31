from fastapi import APIRouter


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['Computers']
)


@router.get('/computers')
async def get_computers():
    return "в разработке"

@router.get('/{computer}')
async def get_computer_by_name(computer: str):
    return "в разработке"

@router.get('/{unit}')
async def get_computers_by_unit(unit: str):  # поиск всех компов в указанном подразделении
    return "в разработке"

@router.post('/{computer}')
async def add_computer_by_name(computer: str):  # добавление компьютера вручную
    return "в разработке"

@router.delete('/{computer}')
async def delete_computer_by_name(computer: str):
    return "в разработке"
