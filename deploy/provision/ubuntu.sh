#!/usr/bin/env bash

export USER=ubuntu
export WORKING_DIR=/srv/kala
export PROJECT=kala
export PROJECT_URL=`curl -s http://169.254.169.254/latest/meta-data/public-hostname`
export HOME=/home/ubuntu
export DEPLOYMENT=dev
export WORKING_DIR=/srv/kala-app
export DATABASE_USER=kala
export DATABASE_PASSWORD=`openssl rand -base64 32`
export DATABASE_NAME=kala
export DATABASE_HOST=localhost
export HOST_NAME=$PROJECT_URL

bash $WORKING_DIR/deploy/provision/provision.sh

