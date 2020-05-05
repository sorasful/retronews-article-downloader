FROM python:3.8.1-slim-buster

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["python", "/app/download_article.py"]