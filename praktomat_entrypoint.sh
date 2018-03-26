#!/bin/bash
/var/www/Praktomat/src/manage-local.py makemigrations
/var/www/Praktomat/src/manage-local.py migrate --noinput
systemctl set-property docker.service TasksMax=4096