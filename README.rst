.. image:: https://travis-ci.org/bgroff/kala-app.svg?branch=master
     :target: https://travis-ci.org/bgroff/kala-app
     :alt: TravisCI

.. image:: https://requires.io/github/bgroff/kala-app/requirements.svg?branch=master
     :target: https://requires.io/github/bgroff/kala-app/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://readthedocs.org/projects/kala-app/badge/?version=latest
     :target: http://kala-app.readthedocs.io/en/latest/
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


=============
Main Features
=============

* People, Companies and Projects can all provide access control
* Written in Python 3 and Django
* MIT License, use as you please
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

You will now be able to open http://localhost:9090 and see the Kala application. There are two users created:

teststaff and testuser both have the password set to test


===========
Screen Shot
===========

.. figure:: https://raw.githubusercontent.com/bgroff/kala-app/master/docs/_images/screenshot.png
   :alt: screenshot of a projects documents

   Showing the Projects page with multiple documents. Each document can have multiple versions. There are additional searching
   and filter options. The settings page allows for configuration of things like permissions and metadata about the various
   objects.


===========
Logo
===========

Designed by linadesteem.
