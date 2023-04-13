from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import computers, organizations, users, auth


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'],
    allow_headers=['*'],
)