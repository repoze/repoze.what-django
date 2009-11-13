***********************************************
:mod:`repoze.what.plugins.dj` API documentation
***********************************************

.. automodule:: repoze.what.plugins.dj


Django middleware
=================

.. autoclass:: RepozeWhatMiddleware
    :members:


In-view functions
=================

These are the functions that are meant to be used in your views:

.. autofunction:: require

.. autofunction:: enforce

.. autofunction:: can_access

.. autofunction:: is_met

.. autofunction:: not_met


Denial handlers
===============

.. automodule:: repoze.what.plugins.dj.denial_handlers
    :members:

