#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import django
import six
import kala
import tests
import sys

sys.path.insert(0, os.path.dirname(kala.__file__))
print(sys.path)
urlpatterns = []

TEMPLATE_DEBUG = True
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = tempfile.mkdtemp(prefix='django_')
DATA_ROOT = os.path.dirname(tests.__file__) + '/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': 'localhost'
    },
}


INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.humanize',
        'django.contrib.staticfiles',

        'kala.kala',
        'kala.accounts',
        'kala.bc_import',
        'kala.companies',
        'kala.documents',
        'kala.projects',

        'tests.accounts',
        'tests.bc_import',
        'tests.companies',
        'tests.documents',
        'tests.projects',

        'django_nose',
]


def runtests(verbosity, interactive, failfast, test_labels):
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=DATABASES,
        AUTH_USER_MODEL='accounts.Person',
        USE_TZ=True,
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
        TEMPLATE_DEBUG=TEMPLATE_DEBUG,
        STATIC_ROOT=os.path.join(TEMP_DIR, 'static'),
        DOCUMENT_ROOT=os.path.join(TEMP_DIR, 'static'),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        SECRET_KEY="kala_tests_secret_key",
        NOSE_ARGS=[
            '--with-coverage',
            '--cover-package=kala.kala,kala.accounts,kala.bc_import,kala.companies,kala.documents,kala.projects'
        ],
        ROOT_URLCONF='kala.kala.urls',
        LOGIN_REDIRECT_URL = '/',
    )

    # Run the test suite, including the extra validation tests.
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    print("Testing against kala installed in '{0}' against django version {1}".format(os.path.dirname(kala.__file__),
                                                                                     django.VERSION))

    test_runner = TestRunner(verbosity=verbosity, interactive=interactive, failfast=failfast)
    failures = test_runner.run_tests(test_labels)
    return failures


def teardown():
    try:
        shutil.rmtree(six.text_type(TEMP_DIR))
    except OSError:
        print('Failed to remove temp directory: %s' % TEMP_DIR)


if __name__ == "__main__":
    from optparse import OptionParser
    usage = "%prog [options] [module module module ...]"
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-v', '--verbosity', action='store', dest='verbosity', default='1',
        type='choice', choices=['0', '1', '2', '3'],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all '
             'output')
    parser.add_option(
        '--noinput', action='store_false', dest='interactive', default=True,
        help='Tells Django to NOT prompt the user for input of any kind.')
    parser.add_option(
        '--failfast', action='store_true', dest='failfast', default=False,
        help='Tells Django to stop running the test suite after first failed '
             'test.')
    options, args = parser.parse_args()

    os.environ['DJANGO_SETTINGS_MODULE'] = 'runtests'
    options.settings = os.environ['DJANGO_SETTINGS_MODULE']

    runtests(int(options.verbosity), options.interactive, options.failfast, args)
