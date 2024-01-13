# pull official base image
FROM python:3.9.2-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install psycopg2 dependencies
RUN apk update \
    && apk add libffi-dev postgresql-dev wkhtmltopdf gcc python3-dev musl-dev py-pip jpeg-dev zlib-dev \
    && apk add libressl-dev perl rust libmagic pango openjpeg-dev g++


COPY requirements/base.txt base.txt
COPY requirements/production.txt production.txt

RUN pip install pip --upgrade  && pip install -r production.txt

COPY . .

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
