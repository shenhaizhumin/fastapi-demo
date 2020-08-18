FROM python:3.8

RUN pip install fastapi uvicorn bcrypt passlib psycopg2-binary PyJWT python-multipart redis requests SQLAlchemy urllib3 uvicorn aiofiles -i https://mirrors.aliyun.com/pypi/simple

EXPOSE 80
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]