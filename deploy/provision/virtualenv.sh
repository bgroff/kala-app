#!/usr/bin/env bash

# Make it so pip does not complain if pip is an older version.
pip install -U pip

# Create the virtualenv
pip install virtualenv
virtualenv -p /usr/bin/python3 /home/vagrant/.virtualenvs/$PROJECT
source /home/vagrant/.virtualenvs/$PROJECT/bin/activate
pip install -r /srv/$PROJECT-app/requirements-dev.txt
chown -R vagrant:vagrant /home/vagrant/.virtualenvs/$PROJECT

# Migrate the database
source /home/vagrant/.zshrc
cd /srv/$PROJECT-app/django_$PROJECT
python3 manage.py migrate

# Create a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print('env = SECRET_KEY={0}'.format(get_random_secret_key()));" >> /etc/uwsgi/apps-available/$PROJECT_URL.ini
