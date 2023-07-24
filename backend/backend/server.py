from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from apscheduler.schedulers.background import BackgroundScheduler
from environs import Env
from loguru import logger

from routers import computers, organizations, users, auth, network, files
from background_tasks import (
    scheduled_generate_customers_cache,
    scheduled_parse_computer_for_unit,
    )


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
        'description': 'работа со статическими файлами.'
    }
]

background = BackgroundScheduler()

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
    expose_headers=['X-Customer-Act', 'X-Customers-Count']
)

logger.add('logs/logs', format='{time:YYYY-MM-DD HH:mm Z} |{file}:{module}:{function}:{line} | {level} | {message}',
        level='INFO', rotation='5 MB',
        compression='tar', backtrace=True, diagnose=True)

@app.get('/check')
async def check():
    return 1

@app.on_event('startup')
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

    background.add_job(
        scheduled_generate_customers_cache.send,
        'cron', day_of_week='0-4', hour='9-17/2' 
    )
    background.add_job(
        scheduled_parse_computer_for_unit.send,
        'cron', day_of_week='0-4', hour='9-18/3'         
    )
    background.start()
    background.print_jobs()

@app.on_event('shutdown')
async def shutdown_event():
    background.shutdown()
