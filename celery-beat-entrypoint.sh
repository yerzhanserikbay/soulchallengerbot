#!/bin/bash

celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler