.. _install:

**************************************
How to install **repoze.what-django**
**************************************

Installing Django
=================

Unfortunately, installing this package is not as easy as it should be because of
Django's limited WSGI support. You need to patch your version of Django to
improve its interoperability and then you'll be able to use WSGI middleware like
:mod:`repoze.what` within Django.

.. note::
    We're trying to get these changes applied in Django and we're maintaining a
    `branch on Bitbucket <https://Gustavo@bitbucket.org/Gustavo/django-wsgi/>`_
    until they are applied.
    
    If they are applied using a different approach to ours, we'll adapt this
    plugin to use the new approach.
    
    Either way, this transition will be totally transparent for you -- You
    would not have to update your code.

If you're using Django 1.1, try the following (on UNIX systems, you should be
able to copy and paste it directly on your terminal):

.. code-block:: bash

    # First, download the patch:
    wget http://what.repoze.org/docs/plugins/django/_static/wsgi-support-django-111.patch
    # Second, `cd` into the directory where Django is installed:
    cd `python -c "from django import __file__ as django_path; print django_path[:-12]"`
    # Finally, apply the patch:
    patch -p0 < wsgi-support-django-111.patch

You may need to adjust the commands above depending on your system.

If you're using the development version of Django 1.2, then try (on UNIX
systems, you should be able to copy and paste it directly on your terminal):

.. code-block:: bash

    # First, clone the branch using Mercurial:
    hg clone https://Gustavo@bitbucket.org/Gustavo/django-wsgi/ django-wsgi
    # Second, cd into the branch:
    cd django-wsgi
    # Finally, install this branch of Django:
    python setup.py install


Installing the plugin
=====================

Once you have a version of Django with the WSGI improvements applied, you'll
be ready to install this plugin and its dependencies.

To get the latest release with :command:`easy_install`, run:

.. code-block:: bash

    easy_install repoze.what-django

Or, if you want to `download a release
<http://pypi.python.org/pypi/repoze.what-django>`_ and install it with
``setuptools``:

.. code-block:: bash

    tar xzf repoze.what-django-1.XXX.tar.gz
    cd repoze.what-django-1.XXX
    python setup.py install

Finally, to install the development version:

.. code-block:: bash

    svn co http://svn.repoze.org/repoze.what/plugins/django/trunk/ repoze.what-django
    cd repoze.what-django
    python setup.py develop

