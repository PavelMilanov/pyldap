from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import computers, organizations, users, auth, network, files
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from db.redis import RedisConnector
from environs import Env
from loguru import logger
from utils.background_tasks import background


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
    },
    {
        'name': 'Files',
        'description': 'обслуживание статических файлов.'
    }
] 

app = FastAPI(
    title='Python LDAP-connector',
    description=description,
    version=env('VERSION'),
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

app.mount("/files", StaticFiles(directory="files"), name="files")

app.include_router(auth.router)
app.include_router(computers.router)
app.include_router(organizations.router)
app.include_router(users.router)
app.include_router(network.router)
app.include_router(files.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[env('ALLOW_ORIGINS')],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'PUT'],
    allow_headers=['*'],
)

logger.add('logs/logs', format='{time:YYYY-MM-DD HH:mm Z} |{file}:{module}:{function}:{line} | {level} | {message}',
        level='INFO', rotation='5 MB',
        compression='tar', backtrace=True, diagnose=True)

@app.on_event("startup")
async def startup_event():
    USER = env('POSTGRES_USER')
    PASSWORD = env('POSTGRES_PASSWORD')
    DB = env('POSTGRES_DB')
    HOST = env('POSTGRES_HOST')

    register_tortoise(
        app,
        db_url=f'postgres://{USER}:{PASSWORD}@{HOST}:5432/{DB}',
        modules={"models": ['db.postgres.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    background.start()

@app.on_event("shutdown")
async def shutdown_event():
    pass
