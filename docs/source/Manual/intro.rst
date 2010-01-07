********************
How the plugin works
********************

**repoze.what-django** allows you to control authorization at several stages
in the request, both before running the views and inside them. It also
provides you with a few utilities to control some authorization bits in your
templates.

The plugin ships with a Django middleware which loads all the access rules
defined across your application when it is run for the first time. 

To start using this plugin, you need to load :mod:`repoze.what`'s middleware
for Django after the authentication middleware::

    # settings.py
    
    MIDDLEWARE_CLASSES = (
        # ...
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "repoze.what.plugins.dj.RepozeWhatMiddleware",
        # ...
    )

