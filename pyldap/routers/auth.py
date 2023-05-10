from fastapi import APIRouter, Depends, Body, Security
from fastapi.security import HTTPAuthorizationCredentials
from utils.connector import domain
from utils.auth import Authentification
from models.schema import AuthSchema

router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)

token_auth_scheme = Authentification()

@router.post('/login')
async def login(form: AuthSchema = Body()):
    resp = await domain.ldap_authentificate(form.username, form.password)
    if resp:
        token = await token_auth_scheme.generate_token(form.username, form.password)
        return token

@router.get('/authentication')
async def authentication(token: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    test = await token_auth_scheme.check_token(token.credentials)
    return True