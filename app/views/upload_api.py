from fastapi import File, UploadFile, APIRouter
from app.response import BaseError, BaseResponse
from app.settings import image_dirname, domain_name

upload_router = APIRouter()


@upload_router.post('/uploadFile')
async def upload_file(file: UploadFile = File(..., alias='image_file')):
    with open(image_dirname.format(filename=file.filename), 'wb') as f:
        bys = await file.read()
        f.write(bys)
    # 返回访问链接
    image_url = domain_name.format(filepath=('/images/{}'.format(file.filename)))
    return BaseResponse(data={
        'image_url': image_url
    })
