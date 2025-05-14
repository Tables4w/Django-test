#!/usr/bin/env bash

# Применение миграций
python manage.py migrate --noinput

# Сборка статики
rm -rf staticfiles/
python manage.py collectstatic