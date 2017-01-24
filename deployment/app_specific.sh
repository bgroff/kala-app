#!/bin/bash
PROJECT=$1
PROJECT_URL=$2

# Load Data
source /home/vagrant/.zshrc
cd /srv/$PROJECT-app/$PROJECT
python3 manage.py migrate
echo "from ndptc.accounts.models import Person; Person.objects.create(**{'address': '1234 st', 'address1': '', 'agency': 'NDPTC', 'citizen': True, 'city': 'Honolulu', 'country_id': 184, 'discipline_id': 10, 'email': 'teststaf@hawaii.edu', 'fema_id': None, 'first_name': 'Test', 'government_level_id': 5, 'is_active': True, 'is_admin': False, 'is_staff': True, 'is_superuser': True, 'is_uh': True, 'last_name': 'Staff', 'middle': '', 'phone': '8089565346', 'state_id': 12, 'title': 'Software Tester', 'username': 'teststaf', 'zip': '96813'});" | python3 manage.py shell
echo "from ndptc.accounts.models import Person; Person.objects.create(**{'address': '1234 st', 'address1': '', 'agency': 'NDPTC', 'citizen': True, 'city': 'Honolulu', 'country_id': 184, 'discipline_id': 10, 'email': 'teststud@hawaii.edu', 'fema_id': None, 'first_name': 'Test', 'government_level_id': 5, 'is_active': True, 'is_admin': False, 'is_staff': False, 'is_superuser': False, 'is_uh': True, 'last_name': 'Student', 'middle': '', 'phone': '8089565346', 'state_id': 12, 'title': 'Software Tester', 'username': 'teststud', 'zip': '96813'});" | python3 manage.py shell

# add the admin static pages.
ln -s /home/vagrant/.virtualenvs/$PROJECT/lib/python3.5/site-packages/django/contrib/admin/static/admin /srv/$PROJECT-app/$PROJECT/$PROJECT/static
ln -s /home/vagrant/.virtualenvs/$PROJECT/lib/python3.5/site-packages/debug_toolbar/static/debug_toolbar /srv/$PROJECT-app/$PROJECT/$PROJECT/static

service uwsgi restart
