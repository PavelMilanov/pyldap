from fastapi import APIRouter, UploadFile, Security
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from typing import Final
import aiofiles, aiofiles.os
from .auth import token_auth_scheme
from db.postgres.models import Act
from models.schema import ActSchema
from loguru import logger


router = APIRouter(
    prefix='/api/v1/files',
    tags=['Files']
)
ACT_DIR: Final = 'files/acts'


@router.post('/act/{customer}/upload')
async def upload_act(
    file: UploadFile,
    customer: str,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> str:
    """Загрузка акта пользователя AD.

    Args:
        file (UploadFile): файл в формате pdf.
        customer (str): имя пользовталя AD.

    Returns:
        str: статус.
    """
    await Act.create(customer=customer, file_name=f'{ACT_DIR}/{customer}.pdf')
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
    return FileResponse(path=file.file, filename=f'{customer}', media_type='multipart/form-data')

@router.put('/act/{customer}/change')
async def change_act(
    file: UploadFile,
    customer: str,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> str:
    """Замена файла для выбранного пользователя.

    Args:
        file (UploadFile): файл в формате pdf.
        customer (str): имя пользовталя AD.

    Returns:
        str: статус.
    """    
    # resp = await Act.get(customer=customer).values()
    # old_file = resp['file_name']
    await aiofiles.os.remove(f'{ACT_DIR}/{customer}.pdf')
    async with aiofiles.open(f'{ACT_DIR}/{customer}.pdf', 'wb') as resp_file:
        content = await file.read()
        await resp_file.write(content)
    resp = await Act.filter(customer=customer).update(file_name=f'{ACT_DIR}/{customer}')
    logger.info(f'Загружен новый акт {file.filename} для {customer}')
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
