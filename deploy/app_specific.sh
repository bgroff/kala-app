#!/bin/bash
PROJECT=$1
PROJECT_URL=$2

# Load Data
source /home/vagrant/.zshrc
cd /srv/$PROJECT-app/django_$PROJECT
python3 manage.py migrate
echo "from accounts.models import User; user = User.objects.create(**{'email': 'teststaff@example.com', 'is_active': True, 'is_staff': True, 'is_superuser': True, 'last_name': 'Staff', 'username': 'teststaff'}); user.set_password('test'); user.save();" | python3 manage.py shell
echo "from accounts.models import User; user = User.objects.create(**{'email': 'testuser@example.com', 'first_name': 'Test', 'is_active': True, 'is_staff': False, 'is_superuser': False, 'last_name': 'User', 'username': 'testuser'}); user.set_password('test'); user.save();" | python3 manage.py shell

# add the admin static pages.
ln -s /home/vagrant/.virtualenvs/$PROJECT/lib/python3.5/site-packages/django/contrib/admin/static/admin /srv/$PROJECT-app/django_$PROJECT/django_$PROJECT/static
ln -s /home/vagrant/.virtualenvs/$PROJECT/lib/python3.5/site-packages/debug_toolbar/static/debug_toolbar /srv/$PROJECT-app/django_$PROJECT/django_$PROJECT/static

service uwsgi restart
