from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import computers, organizations, users, auth, network
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from db.redis import RedisConnector
from environs import Env


env = Env()
env.read_env()

description = """
Python LDAP REST-API
"""

tags_metadata = [
    {
        'name': 'Auth',
        'description': 'аутентификация через домен.'
    },
    {
        'name': 'Computers',
        'description': 'поиск компьютеров в домене.'
    },
    {
        'name': 'Organizations',
        'description': 'поиск подразделений в домене.'
    },
    {
        'name': 'Users',
        'description': 'поиск пользователей в домене.'
    },
    {
        'name': 'Network',
        'description': 'работа с сетью.'
    }
] 

app = FastAPI(
    title='Python LDAP-connector',
    description=description,
    version='0.1.0',
    prefix='/api/',
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url=None,
    openapi_tags=tags_metadata,
    contact={
        'name': 'Pavel Milanov',
        'url': 'https://github.com/PavelMilanov',
        'email': 'pawel.milanov@yandex.ru'
    }
)

app.include_router(auth.router)
app.include_router(computers.router)
app.include_router(organizations.router)
app.include_router(users.router)
app.include_router(network.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[env('ALLOW_ORIGINS')],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'PUT'],
    allow_headers=['*'],
)

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass
