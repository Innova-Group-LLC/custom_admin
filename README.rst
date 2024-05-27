Django Custom Admin
===================

|logo|

A custom admin interface providing backend via DRF and frontend via Vue3
and Vuetify that tries to Keep It Simple.

|PyPI version| |GitHub stars|

`Documentation <https://innova-group-llc.github.io/custom_admin_docs/>`__

Features
--------

-  The web view runs on **Vue 3** using **Vuetify**
-  Pre-builded Vue SPA front page provided through html template and
   static files
-  All endpoints run on Django Rest Framework view-set’s (supports both
   ORM and non-ORM data sources)
-  A powerful inline system with related entities
-  Support for **django-modeltranslation** translations
-  Ability to output any data within inlines (such as external logs with
   pagination)
-  Ability to create admin actions using forms via drf serializers
-  Dynamic system for obtaining partition scheme and interface structure
-  Access rights sharing system based on DRF permissioins
-  Related fields with autocomplete search
-  WYSIWYG editor using TinyMCE 4
-  JSON editor using CodeMirror
-  Related fields Autocomplete and Filters using Vue Tags Input

Vue frontend
============

::

   npm install --prefix vue_frontend
   npm run serve --prefix vue_frontend

Build
-----

::

   npm run build --prefix vue_frontend
   rm -r custom_admin/static/custom_admin/*
   rm -r custom_admin/templates/custom_admin/admin_index.html
   cp vue_frontend/dist/index.html custom_admin/templates/custom_admin/admin_index.html
   cp -r vue_frontend/dist/static/custom_admin/ custom_admin/static/

   python -m build
   python3 -m twine upload --repository pypi dist/*

.. |logo| image:: https://github.com/Innova-Group-LLC/custom_admin/blob/master/logo.png?raw=true
   :target: https://innova-group-llc.github.io/custom_admin_docs/
.. |PyPI version| image:: https://badge.fury.io/py/django-customvueadmin.svg
   :target: https://pypi.org/project/django-customvueadmin/
.. |GitHub stars| image:: https://img.shields.io/github/stars/Innova-Group-LLC/custom_admin
   :target: https://github.com/Innova-Group-LLC/custom_admin
