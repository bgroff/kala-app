FROM registry.access.redhat.com/ubi9/python-311

# Copy in your requirements file
ADD requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
USER 0
RUN pip install --no-cache-dir -r /requirements.txt

ADD deploy/run-local.sh /run-local.sh
RUN chmod +x /run-local.sh
RUN /usr/bin/fix-permissions /run-local.sh

# Get the postgres cli tools for pg_isready
RUN dnf install -y postgresql

USER 1001

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
WORKDIR /code/
ADD django_kala /code/

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=django_kala.settings

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
ENV KALA_DATABASE_USER=''
ENV KALA_DATABASE_PASSWORD=''
ENV KALA_DATABASE_NAME=''
ENV PLATFORM='aws'
ENV KALA_HOST_NAME='localhost'
ENV KALA_AUTHENTICATION_METHOD="login"

RUN python manage.py collectstatic --noinput
RUN cp -r /tmp/static /code/

ADD deploy/uwsgi.ini /uwsgi.ini

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=django_kala/wsgi.py

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/code/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Start uWSGI
CMD ["uwsgi", "--ini", "/uwsgi.ini", "--show-config", "-b", "32768"]
