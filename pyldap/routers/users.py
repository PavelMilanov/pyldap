from fastapi import APIRouter
# from utils.ldap3 import Ldap3Connector
# from models import ldap3


router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['users']
)


@router.get('/')
async def users():
    return "users router"