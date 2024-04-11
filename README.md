# Django Custom Admin

![logo](https://github.com/Innova-Group-LLC/custom_admin/blob/master/logo.png)

A custom admin interface providing backend via DRF and frontend via Vue and Element UI that tries Keep It Simple.

[Documentation](https://innova-group-llc.github.io/custom_admin_docs/)

## Features

- The web view runs on **Vue 2** using **Element UI**
- Pre-builded Vue SPA front page provided through html template and static files
- All endpoints run on Django Rest Framework view-set's (supports both ORM and non-ORM data sources)
- A powerful inline system with related entities
- Support for **django-modeltranslation** translations
- Ability to output any data within inlines (such as external logs with pagination)
- Ability to create admin actions using forms via drf serializers
- Dynamic system for obtaining partition scheme and interface structure
- Access rights sharing system based on DRF permissioins
- Related fields with autocomplete search
- WYSIWYG editor using TinyMCE 4
- JSON editor using CodeMirror
- Related fields Autocomplete and Filters using Vue Tags Input

# Vue frontend

```
npm install --prefix vue_frontend
npm run serve --prefix vue_frontend
```

## Build
```
npm run build --prefix vue_frontend
rm -r custom_admin/static/*
cp vue_frontend/dist/favicon.ico custom_admin/static/favicon.ico
cp vue_frontend/dist/manifest.json custom_admin/static/manifest.json
cp -r vue_frontend/dist/tinymce/ custom_admin/static/tinymce/
cp -r vue_frontend/dist/static/ custom_admin/
```
