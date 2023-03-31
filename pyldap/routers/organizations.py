from fastapi import APIRouter
from utils.connector import domain
from models.domain import Organization


router = APIRouter(
    prefix='/api/v1/ldap3/organizations',
    tags=['organizations']
)


@router.get('/organizations')
async def get_organizations():
    resp = await domain.search_organizations()
    return resp