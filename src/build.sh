#!/bin/bash

echo "BUILD START"

# Create a virtual environment named 'venv' if it doesn't already exist
python -m venv venv

# Activate the virtual environment
# Vercel might not use bash, so you can use the `source` command for bash or `.` for non-bash shells
source venv/bin/activate

# Install dependencies in the virtual environment
pip install -r requirements.txt

# Collect static files using the Python interpreter from the virtual environment
python manage.py collectstatic --noinput

echo "BUILD END"

# [optional] Start the application here if running locally
# python manage.py runserver
