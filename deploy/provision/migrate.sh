# Migrate the database
source $HOME/.bashrc
source $HOME/.virtualenvs/kala/bin/activate
cd /srv/$PROJECT-app/django_$PROJECT
python3 manage.py migrate

# Create a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print('env = SECRET_KEY={0}'.format(get_random_secret_key()));" >> /etc/uwsgi/apps-available/$PROJECT_URL.ini

cat >> $HOME/.bashrc  <<- EOM
export DEPLOYMENT_ENVIRONMENT=$DEPLYOMENT
export DATABASE_USER=$DATABASE_USER
export DATABASE_PASSWORD=$DATABASE_PASSWORD
export DATABASE_NAME=$DATABASE_NAME
export DATABASE_HOST=$DATABASE_HOST
export HOST_NAME=$HOST_NAME
EOM

