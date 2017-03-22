.. Kala documentation master file, created by
   sphinx-quickstart on Fri Mar 17 22:05:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Kala's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


==================
User Documentation
==================

Every person that requires access to the system must be created by an administrator. Once the user has a username and
password, they can then go the login page, which will be the default if the user is not logged in, and log into the
system.

A note about help, every page has a built-in help feature that will provide a guided tour of the pages features and
usages. To access this tour, click on the help button on the navigation bar.

----
Home
----

Once logged in the user will be presented with the "Home Page". From this page the user will see a list of all of the
documents that they have worked on recently. There is also a bar on the right side of the page that is a list of
projects that the user has access too. This list is sorted by companies.

From the Home Page, one can click on any of the links in the **navigation bar**. To access **Projects** and the
associated resources, click on the Projects button.

To get **information about People** that you are working, such as email or phone number you can click on the People
button. The People section of the application is also where and administrator can create new companies and people, more
on this below.

The **help** button will display a guided tour of the features of the page, and can be used as a quick reference of how
to use the application.

In **My Accounts** you can use the **Edit Profile** link to edit your personal information, such as email address, name,
phone, etc... you can also use the My Accounts to logout of the application.

--------
Projects
--------

The Projects page is where you select which project you would like to work with. When you first start on this page you
will be presented with a list of Companies that you are associated with, and a list of the Projects that you are
working on for the Companies.

If you are an administrator you will also be able to **create** new projects from this page. To create a new Project,
you can enter the name of the new Project and select which Company you want to create the Project under. Then click the
"Create Project" button and the new Project will be created. You can also un-delete Projects from this page. Select the
deleted project, then click the Un-delete Project button.

As an administrator you can also **un-delete** a Project from this page by selecting the Project from the "Deleted
Projects" select box, and then by clicking the "Un-delete Project" button. This will also un-delete all of the resources
associated with the Project.


++++++++++++
Project Page
++++++++++++

Once you have selected a Project to work on from the Projects Page, you will be taken to the Project page. This is
where you can interact with the Project's resources. In the Documents tab, you can **upload** a new Document by choosing
the file to upload, the giving the file a description. Once you have done this, you can click the "Upload Document"
button to upload the new Document.

You can also **sort** the Documents either by Date - newest to oldest - or you can sort the Documents alphabetically - A
to Z -. You will need to click the "Sort Documents" button to have the sorting take effect. You can also filter the
Documents by the files type. If you only want to see images in click the "Filter by Category" select box, select images
then click "Sort Documents".

If you would like to **create a new version** of a Document, you can do that from this page as well. To do this, find
the Document that you would like to upload a new version to, then click the "Add Version" link. Follow the same
instructions for uploading a Document as listed above.

If you are an administrator you can also **move** the Project to another Company by click the "Company" select box,
selecting the new Company, then clicking the "Move Project" button.

As and administrator you can also **delete** Project by clicking the "Delete Project" button. Deleting a Project will
also delete all of the resources associated with the Project.

**Un-deleting** Documents can be done by selecting the Document from the Deleted Documents select box and clicking
Un-delete Document button.

Administrators can also **change the permissions** for the Project by clicking on the "Edit Permissions" link in the
breadcrumb below the navigation bar.


+++++++++++++
Document Page
+++++++++++++

On the Document page you can **upload** a new version by following the same steps as above, choose the file, fill out
the description, click upload.

If you are an administrator, you can also **move** a Document to a different Project by selecting the Project in the
"Projects" select box, then clicking the "Move Document" button.

You can also **delete** Documents from this page if you are an administrator.

++++++++++++++++
Edit Permissions
++++++++++++++++

The Edit Permissions page allows an administrator to **grant access** to People for a given Project. The page will
present the administrator with an accordion list of Companies. To grant access to People, click on a Company name, this
will open the accordion, and display a the list of People within the Company. You can then either select/unselect an
individual Person, or you can select/unselect the entire Company. When you have completed your changes, click on the
"Update Permissions" button at the bottom of the page to save the changes you have made.

------
People
------

The People page allows a user to view all of the People that they work with. **If you need to know contact information**
this is the page to look in.

If you are an administrator this page also allows you to **create new Companies** by filling in the Company name, then
clicking on the "Create Company" button. Once the Company has been created an admin can then click on the "Edit" link
next to the Company name to edit the details of the Company.

An administrator can also **create a new Person** by filling in the email address, first name, last name, and selecting
a Company that the Person will be in, then by clicking on the "Create Person" button, a new Person will be created. You
can then edit the details of the Person by clicking the "Edit" link next to the Persons name. **Editing a Person** from
this page will take you to the "Edit Profile" page, which is described below.

An administrator can also un-delete a company by selecting the deleted Company in the "Deleted Companies" select box,
and click the "Un-delete Company" button. This will un-deleted all the People, Projects and resources associated with
the Company.

+++++++++++++++
Company Details
+++++++++++++++

If you click the "Edit" link for a Company, the Company details page will come up. From here you can **edit the
Companies information** such as the website, address, timezone and other information.

You can also **delete** a Company on this page by clicking the "Delete Company" button.

------------
Edit Profile
------------

The Edit Profile page is where you can **edit** either your own information or if you are an administrator, you can edit
the information of other People.

You can also **change your password** or that of others as an administrator from this page, by filling in the password
and confirm text boxes then clicking the "Update Profile" button.

As an administrator you can **delete** a Person here by clicking the "Delete Person", you can also **toggle the
administrative privileges flag** for a Person click clicking the "Grant/Remove Admin" button.

Finally you can grant a Person access to Projects by clicking on the projects tab, then selecting a Company name from
the accordion list, and selecting/unselecting either a single project or you can grant/remove access to all a Companies
projects by clicking the "Select/Unselect All" all checkbox. When you are done, click the "Save Permissions" button.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
