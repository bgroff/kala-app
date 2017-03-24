.. image:: https://requires.io/github/bgroff/kala-app/requirements.svg?branch=master
     :target: https://requires.io/github/bgroff/kala-app/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://readthedocs.org/projects/kala-app/badge/?version=latest
     :target: https://readthedocs.org/projects/kala-app/badge/?version=latest
     :alt: Readthedocs


**********************************
Kala: Project Management in Django
**********************************

Kala is a project management application written in Python on the Django web framework. The intent is for the Kala to
act as a drop in replacement for Basecamp. Kala can import your projects and files from an existing Basecamp
installation. As of the writing of this document, Kala only supports files and file versions, although adding additional
components should relatively straight forward.

Basecamp is a registered trademark of 37signals, LLC and Kala has no affiliation with either.


Kala is the Hawaiian name for surgeonfish and is the mascot for the Kala project management software.

.. image:: https://github.com/bgroff/kala-app/raw/master/django_kala/django_kala/static/img/kala-logo.png
    :alt: Kala logo
    :align: center


=============
Main Features
=============

* People, Companies and Projects can all provide access control
* Written in Python 3 and Django
* MIt License, use as you please
* Easy to use (IMHO)
* Extensible if you know Python and Django

-------


===========
Development
===========

In order to run the development environment, you should install vagrant. Once you have done that you can:

.. code-block:: bash

    $ cd deploy
    $ vagrant up

You will now be able to open http://localhost:8080 and see the Kala application. There are two users created:

teststaff and testuser both have the password set to test
