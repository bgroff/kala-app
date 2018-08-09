#!/usr/bin/env bash

# Make it so pip does not complain if pip is an older version.
sudo pip3 install -U pip virtualenv

virtualenv -p /usr/bin/python3 $HOME/.virtualenvs/$PROJECT
source $HOME/.virtualenvs/$PROJECT/bin/activate
pip install -r /srv/$PROJECT-app/requirements-dev.txt
chown -R $USER:$USER /home/vagrant/.virtualenvs/$PROJECT

