FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL MAINTAINER avishekh@fusemachines.com

WORKDIR /app

COPY requirements_webapi.txt /app/requirements.txt

RUN pip --no-cache-dir install -r requirements.txt

COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]