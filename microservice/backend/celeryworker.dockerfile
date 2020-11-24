FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL MAINTAINER avishekh@fusemachines.com

COPY requirements_celery.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./celery /celery_tasks
WORKDIR /celery_tasks

ENTRYPOINT celery -A tasks worker --loglevel=info