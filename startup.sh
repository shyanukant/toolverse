#!/bin/bash

# Define the path to your virtual environment
venv_path=/home/site/wwwroot/antenv

# Activate the virtual environment
source $venv_path/bin/activate

# Change directory to your Django app's root folder
cd /home/site/wwwroot

# Install dependencies from requirements.txt (optional, but good practice)
pip install -r requirements.txt

# Run your Django app using Gunicorn
gunicorn toolverse.wsgi:application --bind 0.0.0.0:$PORT