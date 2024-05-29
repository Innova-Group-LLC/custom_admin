Django Custom Admin
===================

|logo|

A custom admin interface providing backend via DRF and frontend via Vue3
and Vuetify that tries to Keep It Simple.

|PyPI version| |GitHub stars|

`Documentation <https://innova-group-llc.github.io/custom_admin_docs/>`__

Features
--------

- Interface for [DRF](https://www.django-rest-framework.org/) API based on **[Vue 3](https://vuejs.org/)** and **[Vuetify](https://vuetifyjs.com/)**
- Pre-builded Vue SPA front page provided through [Django](https://www.djangoproject.com/) template/static files. A separate setup for the front end is not required.
- Ability to create inline admin actions using forms via DRF serializers
- Dynamic system for obtaining partition scheme and interface structure
- Access rights sharing system based on DRF permissioins

**Custom fields**
- Related fields/filters with autocomplete search
- WYSIWYG editor using [TinyMCE](https://www.tiny.cloud/docs/tinymce/latest/)
- JSON editor using [svelte-jsoneditor](https://github.com/josdejong/svelte-jsoneditor) and [JSONForms](https://jsonforms.io/)
- Autocomplete for related fields and filters using API
- Support for [django-modeltranslation](https://readthedocs.org/projects/django-modeltranslation/) translations

**Non ORM inlines**
- Table views
- Support for graphs using [chartjs](https://www.chartjs.org/)

Vue frontend
============

::

   npm install --prefix vue_frontend
   npm run dev --prefix vue_frontend

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
