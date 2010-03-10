# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009-2010, Gustavo Narea <me@gustavonarea.net>.
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

__all__ = ("IsStaff", "IsActive", "IsSuperuser", "IS_STAFF", "IS_ACTIVE",
           "IS_SUPERUSER")


class IsStaff(Predicate):
    """
    Check that the current user can access the Django's admin site.
    
    Under the hood, it uses ``request.user.is_staff``.
    
    """
    
    def check(self, request, credentials):
        return request.user.is_staff


class IsActive(Predicate):
    """
    Check that the account for the current user is active.
    
    Under the hood, it uses ``request.user.is_active``.
    
    """
    
    def check(self, request, credentials):
        return request.user.is_active


class IsSuperuser(Predicate):
    """
    Check that the current user is admin.
    
    Under the hood, it uses ``request.user.is_superuser``.
    
    """
    
    def check(self, request, credentials):
        return request.user.is_superuser


#{ Ready to use instances


IS_STAFF = IsStaff()

IS_ACTIVE = IsActive()

IS_SUPERUSER = IsSuperuser()


#}

