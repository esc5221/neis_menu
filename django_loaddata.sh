#!/bin/sh
docker exec neis_menu_django_1 python3 manage.py loaddata _dumped_data/schools.json
docker exec neis_menu_django_1 python3 manage.py loaddata _dumped_data/menus.json