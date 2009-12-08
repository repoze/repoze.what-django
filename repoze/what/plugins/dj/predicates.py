# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009, Gustavo Narea <me@gustavonarea.net>.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Django-specific :mod:`repoze.what` predicates.

"""

from repoze.what.predicates import Predicate

__all__ = ("is_staff", "is_active", "is_superuser", "has_module_perms")


class is_staff(Predicate):
    """
    Check that the current user can access the Django's admin site.
    
    Under the hood, it uses ``request.user.is_staff``.
    
    """
    
    message = u"The current user must belong to the staff"
    
    def evaluate(self, environ, credentials):
        if not credentials['django_user'].is_staff:
            self.unmet()


class is_active(Predicate):
    """
    Check that the account for the current user is active.
    
    Under the hood, it uses ``request.user.is_active``.
    
    """
    
    message = u"The account for the current user must be active"
    
    def evaluate(self, environ, credentials):
        if not credentials['django_user'].is_active:
            self.unmet()


class is_superuser(Predicate):
    """
    Check that the current user is admin.
    
    Under the hood, it uses ``request.user.is_superuser``.
    
    """
    
    message = u"The current user must be a superuser"
    
    def evaluate(self, environ, credentials):
        if not credentials['django_user'].is_superuser:
            self.unmet()

