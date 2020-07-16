from fastapi import File, UploadFile, APIRouter
from app.response import BaseError, BaseResponse
from app.settings import image_dirname, domain_name
import os.path

upload_router = APIRouter()


@upload_router.post('/uploadFile')
async def upload_file(file: UploadFile = File(..., alias='image_file')):
    bys = await file.read()
    if not bys:
        raise BaseError(msg='missing file or file is empty')
    with open(image_dirname.format(filename=file.filename), 'wb') as f:
        f.write(bys)
    # 返回访问链接
    image_url = domain_name.format(filepath=('/images/{}'.format(file.filename)))
    return BaseResponse(data={
        'image_url': image_url
    })
