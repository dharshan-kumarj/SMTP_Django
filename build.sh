#!/usr/bin/env bash
# filepath: \\wsl.localhost\Ubuntu\home\jd\projects\SMTP_Django\build.sh
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate