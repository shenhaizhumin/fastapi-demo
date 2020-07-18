from fastapi import File, UploadFile, APIRouter
from app.response import BaseError, BaseResponse
from app.settings import image_dirname, domain_name
from typing import List
import os.path
from app.models.file_entity import FileEntity

upload_router = APIRouter()


@upload_router.post('/uploadFile')
async def upload_file(file: UploadFile = File(..., alias='image_file')):
    bys = await file.read()
    if not bys:
        raise BaseError(msg='missing file or file is empty')
    file_path = image_dirname.format(filename=file.filename)
    with open(file_path, 'wb') as f:
        f.write(bys)
    # 返回访问链接
    image_url = domain_name.format(filepath=('/images/{}'.format(file.filename)))
    file_entity = FileEntity(file_name=file.filename, file_path=file_path, file_url=image_url)

    return BaseResponse(data=file_entity)


@upload_router.post('/uploadFiles')
async def upload_files(file_list: List[UploadFile] = File(...)):
    file_entities = []
    for file in file_list:
        bys = await file.read()
        if not bys:
            raise BaseError(msg='missing file or file is empty')
        file_path = image_dirname.format(filename=file.filename)
        with open(file_path, 'wb') as f:
            f.write(bys)
        # 返回访问链接
        image_url = domain_name.format(filepath=('/images/{}'.format(file.filename)))
        file_entity = FileEntity(file_name=file.filename, file_path=file_path, file_url=image_url)
        file_entities.append(file_entity)
    return BaseResponse(data=file_entities)
