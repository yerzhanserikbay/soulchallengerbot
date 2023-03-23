FROM python:3.10.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && pip install --upgrade pip && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    libev-dev \
    gcc \
    htop \
    locales  \
    locales-all

COPY . /project
WORKDIR /project


RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir && \
    rm -rf ~/.cache/pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge   --auto-remove && \
    apt-get clean


COPY django-entrypoint.sh /scripts/
COPY celery-entrypoint.sh /scripts/
COPY celery-beat-entrypoint.sh /scripts/

RUN chmod +x /scripts/django-entrypoint.sh && \
    chmod +x /scripts/celery-entrypoint.sh && \
    chmod +x /scripts/celery-beat-entrypoint.sh
