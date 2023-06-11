from fastapi import APIRouter, UploadFile


router = APIRouter(
    prefix='/api/v1/files',
    tags=['Files']
)


@router.post('/act')
async def upload_act(file: UploadFile):
    return {"filename": file.filename}
