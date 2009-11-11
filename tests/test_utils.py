# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
Tests for the utilities denied at :mod:`repoze.what.plugins.dj.utils`.

"""

from nose.tools import eq_, ok_, assert_false

from repoze.what.plugins.dj import is_met, not_met, enforce
from repoze.what.plugins.dj.utils import _AuthorizationDenial

from tests import Request, make_user, MockPredicate


class TestIsMet(object):
    """Tests for the is_met() function."""
    
    def test_with_predicate_met(self):
        req = Request({}, make_user(None))
        ok_(is_met(MockPredicate(), req))
    
    def test_with_predicate_unmet(self):
        req = Request({}, make_user(None))
        assert_false(is_met(MockPredicate(False), req))


class TestNotMet(object):
    """Tests for the not_met() function."""
    
    def test_with_predicate_met(self):
        req = Request({}, make_user(None))
        assert_false(not_met(MockPredicate(), req))
    
    def test_with_predicate_unmet(self):
        req = Request({}, make_user(None))
        ok_(not_met(MockPredicate(False), req))


class TestEnforcer(object):
    """Tests for the enforce() function."""
    
    def test_with_predicate_met(self):
        req = Request({}, make_user(None))
        enforce(MockPredicate(), req)
    
    def test_with_predicate_unmet(self):
        req = Request({}, make_user(None))
        self._check_enforcement(MockPredicate(False), req)
    
    def test_with_predicate_unmet_with_message(self):
        req = Request({}, make_user(None))
        self._check_enforcement(MockPredicate(False), req,
                                expected_message="Go away")
    
    def test_with_predicate_unmet_with_denial_handler(self):
        req = Request({}, make_user(None))
        self._check_enforcement(MockPredicate(False), req,
                                expected_denial_handler=object())
    
    def test_with_predicate_unmet_with_message_and_denial_handler(self):
        req = Request({}, make_user(None))
        self._check_enforcement(MockPredicate(False), req,
                                expected_message="Go away",
                                expected_denial_handler=object())
    
    def _check_enforcement(self, predicate, request, expected_message=None,
                           expected_denial_handler=None):
        """Make sure ``predicate`` is not met and enforced as expected."""
        try:
            enforce(predicate, request, expected_message,
                    expected_denial_handler)
        except _AuthorizationDenial, authz_denial:
            eq_(authz_denial.reason, expected_message)
            eq_(authz_denial.handler, expected_denial_handler)
        else:
            raise AssertionError("Authorization denial not raised")

