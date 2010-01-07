*********************
Creating access rules
*********************

Everything can protected with repoze.what: The entire project, an entire
application, groups of applications, individual views and/or groups of views.

There are three ways to protect your Django project with repoze.what and it's
OK to use more than one:


Using Access Control Lists
==========================




Enforcing conditions inside a view
==================================


.. note::

    When using this method, it's impossible to tell whether authorization would
    be granted to said view from the outside. As consequence,
    :func:`repoze.what.plugins.dj.can_access` won't take the condition into
    account and will report that access would be granted.
    
    This wouldn't be an issue if you don't use that function on that view.


With a decorator in the views
=============================

