#!/bin/bash

celery -A config.celery worker --loglevel=info -Q new_cars --concurrency=5