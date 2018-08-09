#!/usr/bin/env bash

# Make it so pip does not complain if pip is an older version.
sudo pip3 install -U pip virtualenv

virtualenv -p /usr/bin/python3 /home/vagrant/.virtualenvs/$PROJECT
source /home/vagrant/.virtualenvs/$PROJECT/bin/activate
pip install -r /srv/$PROJECT-app/requirements-dev.txt
chown -R vagrant:vagrant /home/vagrant/.virtualenvs/$PROJECT

