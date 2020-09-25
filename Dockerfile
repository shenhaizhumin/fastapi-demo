FROM python:3.8

COPY ./app /app
COPY ./requirements.txt /app
COPY ./configs.yml /
RUN pip3 install -r /app/requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8031"]
