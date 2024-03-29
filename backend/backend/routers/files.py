from fastapi import APIRouter, UploadFile, Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from typing import Final
import aiofiles
import aiofiles.os
from loguru import logger

from .auth import token_auth_scheme
from db.postgres.models import Act
from models.schema import ActSchema


router = APIRouter(
    prefix='/api/v1/files',
    tags=['Files']
)
ACT_DIR: Final = 'files/acts'


@router.post('/act/{customer}/upload')
async def upload_act(
    file: UploadFile,
    customer: str,
    name: str = None,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> str:
    """Загрузка акта пользователя AD.

    Args:
        file (UploadFile): файл в формате pdf.
        customer (str): имя пользовталя AD.

    Returns:
        str: статус.
    """
    await Act.create(customer=customer, name=name, file_name=f'{ACT_DIR}/{customer}.pdf')
    async with aiofiles.open(f'{ACT_DIR}/{customer}.pdf', 'wb') as resp_file:
        content = await file.read()
        await resp_file.write(content)
        logger.info(f'Загружен акт {file.filename} для {customer}')
    return 'ok'

@router.get('/act/{customer}/download')
async def download_act(
    customer: str,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> FileResponse:
    """Скачивание акта пользователя AD.

    Args:
        customer (str): имя пользователя AD.

    Returns:
        FileResponcse: файл pdf.
    """    
    resp = await Act.get(customer=customer).values()
    file = ActSchema(**resp)
    return FileResponse(
        path=file.file,
        filename=f'{customer}',
        media_type='multipart/form-data'
        )

@router.put('/act/{customer}/change')
async def change_act(
    customer: str,
    file: UploadFile = None,
    name: str = None,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> str:
    """Замена файла для выбранного пользователя.

    Args:
        file (UploadFile): файл в формате pdf.
        customer (str): имя пользовталя AD.

    Returns:
        str: статус.
    """
    if file:
        await aiofiles.os.remove(f'{ACT_DIR}/{customer}.pdf')
        async with aiofiles.open(f'{ACT_DIR}/{customer}.pdf', 'wb') as resp_file:
            content = await file.read()
            await resp_file.write(content)
        await Act.filter(customer=customer).update(file_name=f'{ACT_DIR}/{customer}')
        logger.info(f'Загружен новый акт {file.filename} для {customer}')
    if name:
        await Act.filter(customer=customer).update(name=name)
        logger.info(f'Изменено описание для {customer}')
    return 'ok'

@router.delete('/act/{customer}/delete')
async def delete_act(
    customer: str,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> str:
    """Удаление файла и записи.

    Args:
        customer (str): имя пользовталя AD.

    Returns:
        str: статус.
    """    
    await Act.get(customer=customer).delete()
    await aiofiles.os.remove(f'{ACT_DIR}/{customer}.pdf')
    logger.info(f'Удален акт для {customer}')
    return 'ok'

@router.get('/acts')
async def get_acts(token: HTTPAuthorizationCredentials = Security(token_auth_scheme)) -> list:
    """_summary_

    Args:
        token (HTTPAuthorizationCredentials, optional): _description_. Defaults to Security(token_auth_scheme).

    Returns:
        dict: _description_
    """    
    acts = await Act.all().values()
    return acts
