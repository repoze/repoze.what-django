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
Unit tests for the Django-specific repoze.what predicates.

"""

from nose.tools import eq_, ok_, assert_false

from repoze.what.predicates import NotAuthorizedError

from repoze.what.plugins.dj import (RepozeWhatMiddleware, IsStaff, IsActive,
                                    IsSuperuser, IS_STAFF, IS_ACTIVE,
                                    IS_SUPERUSER)
from tests import Request, make_user


class BasePredicateTester(object):
    """Base test case for predicates."""
    
    def setUp(self):
        """Set up the request."""
        mw = RepozeWhatMiddleware()
        self.request = Request({}, make_user("foo"))
        mw._set_request_up(self.request)


class TestIsStaff(BasePredicateTester):
    """Tests for the :class:`IsStaff` predicate."""
    
    def test_non_staff_user(self):
        """
        The predicate must not be met if the user doesn't belong to the staff.
        
        """
        self.request.user.is_staff = False
        assert_false(IS_STAFF(self.request),
                     "The current user must belong to the staff")
    
    def test_staff_user(self):
        """
        The predicate must be met if the user DOES belong to the staff.
        
        """
        self.request.user.is_staff = True
        ok_(IS_STAFF(self.request))
    
    def test_alias(self):
        ok_(isinstance(IS_STAFF, IsStaff))


class TestIsActive(BasePredicateTester):
    """Tests for the :class:`IsActive` predicate."""
    
    def test_inactive_account(self):
        """
        The predicate must not be met if the user's account is inactive.
        
        """
        self.request.user.is_active = False
        assert_false(IS_ACTIVE(self.request),
                     "The account for the current user must be active")
    
    def test_active_account(self):
        """
        The predicate must be met if the user's account is active.
        
        """
        self.request.user.is_active = True
        ok_(IS_ACTIVE(self.request))
    
    def test_alias(self):
        ok_(isinstance(IS_ACTIVE, IsActive))


class TestIsSuperuser(BasePredicateTester):
    """Tests for the :class:`IsSuperuser` predicate."""
    
    def test_regular_user(self):
        """
        The predicate must not be met if the user is not admin.
        
        """
        self.request.user.is_superuser = False
        assert_false(IS_SUPERUSER(self.request),
                     "The current user must be a superuser")
    
    def test_superuser_account(self):
        """
        The predicate must be met if the user is an admin.
        
        """
        self.request.user.is_superuser = True
        ok_(IS_SUPERUSER(self.request))
    
    def test_alias(self):
        ok_(isinstance(IS_SUPERUSER, IsSuperuser))

