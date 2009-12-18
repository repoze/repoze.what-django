***********************************************
:mod:`repoze.what.plugins.dj` API documentation
***********************************************

.. automodule:: repoze.what.plugins.dj


In-view functions
=================

These are the functions that are meant to be used in your views:

.. autofunction:: require

.. autofunction:: enforce

.. autofunction:: can_access

.. autofunction:: is_met

.. autofunction:: not_met


Django-specific predicate checkers
==================================

.. autoclass:: IsStaff

.. autoclass:: IsActive

.. autoclass:: IsSuperuser

Ready to use instances
----------------------

.. autodata:: IS_STAFF

.. autodata:: IS_ACTIVE

.. autodata:: IS_SUPERUSER


Django middleware
=================

.. autoclass:: RepozeWhatMiddleware
    :members:


Denial handlers
===============

.. automodule:: repoze.what.plugins.dj.denial_handlers
    :members:

