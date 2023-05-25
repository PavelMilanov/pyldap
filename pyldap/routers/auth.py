from fastapi import APIRouter, Body, Security
from fastapi.security import HTTPAuthorizationCredentials
from utils.auth import Authentification
from models.schema import AuthSchema
from .import ldap


router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)

token_auth_scheme = Authentification()

@router.post('/login')
async def login(form: AuthSchema = Body()) -> str:
    """Авторизация под пользователем в домене.
    При успешной авторизации возврашает токен/

    Args:
        form (AuthSchema, optional): {
            username: str,
            password: str
            }. Defaults to Body().

    Returns:
        str: токен авторизации.
    """    
    resp = await ldap.ldap_authentificate(form.username, form.password)
    if resp:
        token = await token_auth_scheme.generate_token(form.username, form.password)
        return token

@router.get('/authentication')
async def authentication(token: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    """Аутентификая по токену.
    Args:
        token (HTTPAuthorizationCredentials, optional): _description_. Defaults to Security(token_auth_scheme).
    """    
    token = await token_auth_scheme.check_token(token.credentials)
