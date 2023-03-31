from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import computers, organizations, users


description = """
Python LDAP REST-API
"""

tags_metadata = [
    {
        'name': 'auth',
        'description': 'аутентификация.'
    },
    {
        'name': 'computers',
        'description': 'поиск компьютеров в домене.'
    },
    {
        'name': 'organizations',
        'description': 'поиск подразделений в домене.'
    },
    {
        'name': 'users',
        'description': 'поиск пользователей в домене.'
    },
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

app.include_router(computers.router)
app.include_router(organizations.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=['*'],
)