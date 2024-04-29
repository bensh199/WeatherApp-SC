FROM python:alpine3.19 AS build
# RUN apt update -y && apt install -y python3 python3-pip python3-venv
COPY . /app/
WORKDIR /app
RUN pip install gunicorn Flask requests boto3 elasticsearch
RUN chmod +x init.sh
CMD gunicorn -w 3 -b 0.0.0.0:8000 main:app