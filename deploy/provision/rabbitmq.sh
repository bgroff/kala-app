#!/usr/bin/env bash

apt install -y rabbitmq-server
rabbitmqctl add_user kala kala
rabbitmqctl set_user_tags kala administrator
rabbitmqctl set_permissions -p / kala ".*" ".*" ".*"
