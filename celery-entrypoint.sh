#!/bin/bash

celery -A config.celery worker --loglevel=info --concurrency=5