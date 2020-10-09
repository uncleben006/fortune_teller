FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y nginx && \
    apt-get install -y curl && \
    apt-get install -y vim && \
    apt-get install -y redis && \
    apt-get install -y postgresql postgresql-contrib python-psycopg2 libpq-dev && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

COPY ./fortune_nginx.conf /etc/nginx/sites-available/fortune_nginx.conf
COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install uwsgi

EXPOSE 443
EXPOSE 80