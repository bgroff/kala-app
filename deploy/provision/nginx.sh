#!/usr/bin/env bash


# Clear out the nginx config if needed
if [ -f /etc/nginx/sites-available/default ]; then
    rm /etc/nginx/sites-enabled/default
    rm /etc/nginx/sites-available/default
fi

# Create the nginx conf
cat > /etc/nginx/sites-available/$PROJECT_URL.conf <<- EOM
server {
    listen   80;

    charset utf-8;
    server_name $PROJECT_URL;
    access_log /var/log/nginx/$PROJECT_URL.access.log;
    error_log /var/log/nginx/$PROJECT_URL.error.log;
    client_max_body_size 200M;
    sendfile off;

    location / {
        uwsgi_pass unix:/run/uwsgi/app/$PROJECT_URL/socket;
        include    uwsgi_params;
    }

    location /static/ {
            alias /srv/$PROJECT-app/django_$PROJECT/django_$PROJECT/static/;
    }

    location /media/ {
            alias /srv/$PROJECT-app/django_$PROJECT/django_$PROJECT/media/;
    }
}
EOM

# If the symbolic link exists, remove it.
if [ -f /etc/nginx/sites-enabled/$PROJECT_URL.conf ]; then
    rm /etc/nginx/sites-enabled/$PROJECT_URL.conf
fi
ln -s /etc/nginx/sites-available/$PROJECT_URL.conf /etc/nginx/sites-enabled/$PROJECT_URL.conf
