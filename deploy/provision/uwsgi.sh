#!/usr/bin/env bash

# Clear out the uwsgi config if needed
if [ -f /etc/uwsgi/apps-available/README ]; then
    rm /etc/uwsgi/apps-enabled/README
    rm /etc/uwsgi/apps-available/README
fi


# Create the uwsgi conf
cat > /etc/uwsgi/apps-available/$PROJECT_URL.ini <<- EOM
[uwsgi]
vhost = true
plugins = python3
master = true
enable-threads = true
processes = 2
chdir = /srv/$PROJECT-app/django_$PROJECT
module = django_$PROJECT.wsgi:application
touch-reload = /srv/$PROJECT-app/reload
virtualenv = /home/vagrant/.virtualenvs/$PROJECT

env = DEPLOYMENT_ENVIRONMENT=$DEPLOYMENT
env = DATABASE_USER=$DATABASE_USER
env = DATABASE_PASSWORD=$DATABASE_PASSWORD
env = DATABASE_NAME=$DATABASE_NAME
env = DATABASE_HOST=$DATABASE_HOST
env = HOST_NAME=$HOST_NAME
EOM


# If the symbolic link exists, remove it.
if [ -f /etc/uwsgi/apps-enabled/$PROJECT_URL.ini ]; then
    rm /etc/uwsgi/apps-enabled/$PROJECT_URL.ini
fi
ln -s /etc/uwsgi/apps-available/$PROJECT_URL.ini /etc/uwsgi/apps-enabled/$PROJECT_URL.ini
