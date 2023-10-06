#!/bin/bash
export PYTHONPATH=$PYTHONPATH:"/home/site/wwwroot/.venv/lib/site-packages"

# Install dependencies from requirements.txt (optional, but good practice)
pip install -r requirements.txt

# Run your Django app using Gunicorn
GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' --chdir=/home/site/wwwroot" gunicorn  toolverse.wsgi:application --bind 0.0.0.0:$PORT