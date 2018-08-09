#!/usr/bin/env bash

export PROJECT=$1
export PROJECT_URL=$2
export USER=vagrant
export HOME=/home/vagrant
export DEPLOYMENT=dev
export WORKING_DIR=/srv/kala-app
export DATABASE_USER=kala
export DATABASE_PASSWORD=kala
export DATABASE_NAME=kala
export DATABASE_HOST=localhost
export HOST_NAME=localhost

bash $WORKING_DIR/deploy/provision/provision.sh
