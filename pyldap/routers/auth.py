from fastapi import APIRouter, Depends, Body
from utils.connector import domain
from fastapi.security import OAuth2PasswordBearer
from utils.auth import auth
from models.schema import AuthSchema


router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)

auth_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/')

async def ldap_auth(token: str = Depends(auth_scheme)):
    resp = await auth.check_token(token)
    print(resp)

@router.post('/')
async def authentificate(form: AuthSchema = Body()):
    resp = await domain.ldap_authentificate(form.username, form.password)
    if resp:
        token = await auth.generate_token(form.username, form.password)
        return token

@router.get('/me')
async def me(token: str = Depends(ldap_auth)):
    return 'в разработке'