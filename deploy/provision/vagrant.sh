#!/usr/bin/env bash

export PROJECT=$1
export PROJECT_URL=$2
export DEPLOYMENT=dev
export WORKING_DIR=/vagrant
export DATABASE_USER=kala
export DATABASE_PASSWORD=kala
export DATABASE_NAME=kala
export HOST_NAME=kala

bash $WORKING_DIR/deploy/provision/virtualenv.sh
