#!/bin/sh
pip3 install --user -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 0:8000