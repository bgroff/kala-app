#!/usr/bin/env bash

apt install -y postgresql

# Create the database, check if the role and database exist first though.
if ! sudo -u postgres -- psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='kala'" | grep -q 1; then
	sudo -u postgres -- psql -c "CREATE ROLE kala WITH LOGIN PASSWORD 'kala';"
fi

if ! sudo -u postgres -- psql -tAc "SELECT 1 from pg_database WHERE datname='kala'"  | grep -q 1; then
	sudo -u postgres -- psql -c "CREATE DATABASE kala WITH OWNER kala;"
fi

# Load Data
source /home/vagrant/.zshrc
cd /srv/$PROJECT-app/django_$PROJECT
python3 manage.py migrate
echo "from auth.models import User; user = User.objects.create(**{'email': 'teststaff@example.com', 'is_active': True, 'is_staff': True, 'is_superuser': True, 'last_name': 'Staff', 'username': 'teststaff'}); user.set_password('test'); user.save();" | python3 manage.py shell
echo "from auth.models import User; user = User.objects.create(**{'email': 'testuser@example.com', 'first_name': 'Test', 'is_active': True, 'is_staff': False, 'is_superuser': False, 'last_name': 'User', 'username': 'testuser'}); user.set_password('test'); user.save();" | python3 manage.py shell
# Create the organization and a project
echo "from organizations.models import Organization; Organization.objects.create(name='Test Organization')" | python3 manage.py shell
echo "from organizations.models import Organization; from projects.models import Project; Project.objects.create(name='Test Project', organization=Organization.objects.get(name='Test Organization'))" | python3 manage.py shell
# Add the staff to the organization
echo "from organizations.models import Organization; from projects.models import Project; from auth.models import User, Permissions, Permission; Permissions.objects.create(user=User.objects.get(email='teststaff@example.com'), permission=Permission.objects.get(codename='add_organization'), object_uuid=Organization.objects.get(name='Test Organization').uuid)" | python3 manage.py shell
echo "from organizations.models import Organization; from projects.models import Project; from auth.models import User, Permissions, Permission; Permissions.objects.create(user=User.objects.get(email='teststaff@example.com'), permission=Permission.objects.get(codename='change_organization'), object_uuid=Organization.objects.get(name='Test Organization').uuid)" | python3 manage.py shell
echo "from organizations.models import Organization; from projects.models import Project; from auth.models import User, Permissions, Permission; Permissions.objects.create(user=User.objects.get(email='teststaff@example.com'), permission=Permission.objects.get(codename='delete_organization'), object_uuid=Organization.objects.get(name='Test Organization').uuid)" | python3 manage.py shell
# Add the user to the project
echo "from organizations.models import Organization; from projects.models import Project; from auth.models import User, Permissions, Permission; Permissions.objects.create(user=User.objects.get(email='testuser@example.com'), permission=Permission.objects.get(codename='add_project'), object_uuid=Project.objects.get(name='Test Project').uuid)" | python3 manage.py shell
echo "from organizations.models import Organization; from projects.models import Project; from auth.models import User, Permissions, Permission; Permissions.objects.create(user=User.objects.get(email='testuser@example.com'), permission=Permission.objects.get(codename='change_project'), object_uuid=Project.objects.get(name='Test Project').uuid)" | python3 manage.py shell
echo "from organizations.models import Organization; from projects.models import Project; from auth.models import User, Permissions, Permission; Permissions.objects.create(user=User.objects.get(email='testuser@example.com'), permission=Permission.objects.get(codename='delete_project'), object_uuid=Project.objects.get(name='Test Project').uuid)" | python3 manage.py shell

# add the admin static pages.
ln -s /home/vagrant/.virtualenvs/$PROJECT/lib/python3.5/site-packages/django/contrib/admin/static/admin /srv/$PROJECT-app/django_$PROJECT/django_$PROJECT/static
ln -s /home/vagrant/.virtualenvs/$PROJECT/lib/python3.5/site-packages/debug_toolbar/static/debug_toolbar /srv/$PROJECT-app/django_$PROJECT/django_$PROJECT/static

service uwsgi restart
