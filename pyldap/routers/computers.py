from fastapi import APIRouter
# from utils.ldap3 import Ldap3Connector
# from models import ldap3


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['computers']
)


@router.get('/')
async def computers():
    return "computers router"