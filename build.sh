#!/usr/bin/env bash

# Применение миграций
python manage.py migrate --noinput

# Сборка статики
python manage.py collectstatic --noinput