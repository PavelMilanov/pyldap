from fastapi import APIRouter, Depends, Body, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.connector import domain
from utils.auth import auth
from models.schema import AuthSchema

router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)

security = HTTPBearer()

async def verify(token):
    resp = await auth.check_token(token)
    print(resp)

@router.post('/')
async def registration(form: AuthSchema = Body()):
    resp = await domain.ldap_authentificate(form.username, form.password)
    if resp:
        token = await auth.generate_token(form.username, form.password)
        return token

@router.get('/me')
async def me(token: HTTPAuthorizationCredentials = Security(security)):
      test = await verify(token.credentials)
      return True