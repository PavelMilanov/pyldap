from fastapi import APIRouter
from utils.connector import domain
from models.domain import Organization


router = APIRouter(
    prefix='/api/v1/ldap3/organizations',
    tags=['organizations']
)

@router.get('/schema')
async def get_organizations_schema():
    resp = await domain.search_organizations_schema()
    return resp

@router.get('/tree')
async def get_organizations_tree():
    resp = await domain.search_organizations_tree()
    return resp