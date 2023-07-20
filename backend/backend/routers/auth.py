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
async def login(form: AuthSchema = Body()) -> str | None:
    """Авторизация под пользователем в домене.
    При успешной авторизации возврашает токен/

    Args:
        form (AuthSchema, optional): {
            username: str,
            password: str
            }. Defaults to Body().

    Returns:
        str | None: токен авторизации.
    """    
    resp = await ldap.ldap_authentificate(form.username, form.password)
    if resp:
        token = await token_auth_scheme.generate_token(form.username, form.password)
        return token
