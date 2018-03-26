#!/bin/bash
if [ ! -f /tmp/init-script-completed ]; then
    /var/www/Praktomat/src/manage-local.py makemigrations
    /var/www/Praktomat/src/manage-local.py migrate --noinput

    touch /tmp/init-script-completed
fi