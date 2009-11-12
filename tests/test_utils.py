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

from nose.tools import eq_, ok_, assert_false, assert_raises

from django.core.urlresolvers import Resolver404
from repoze.what.plugins.dj import (is_met, not_met, enforce, require,
                                    can_access, RepozeWhatMiddleware)
from repoze.what.plugins.dj.utils import _AuthorizationDenial

from tests import Request, make_user, MockPredicate
from tests.fixtures.loggers import LoggingHandlerFixture


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
    

class TestRequire(object):
    """Tests for the @require decorator."""
    
    def setUp(self):
        self.req = Request({}, make_user(None))
    
    def test_require_with_predicate_met(self):
        protected_view = require(MockPredicate())(mock_view)
        eq_(protected_view(self.req), "Got it")
    
    def test_require_with_predicate_unmet(self):
        protected_view = require(MockPredicate(False))(mock_view)
        self._check_enforcement(protected_view)
    
    def test_require_with_predicate_unmet_with_message(self):
        protected_view = require(MockPredicate(False), "Go away")(mock_view)
        self._check_enforcement(protected_view, expected_message="Go away")
    
    def test_require_with_predicate_unmet_with_denial_handler(self):
        denial_handler = object()
        protected_view = require(
            MockPredicate(False),
            denial_handler=denial_handler,
            )(mock_view)
        self._check_enforcement(protected_view,
                                expected_denial_handler=denial_handler)
    
    def test_require_with_predicate_unmet_with_message_and_denial_handler(self):
        denial_handler = object()
        protected_view = require(
            MockPredicate(False),
            "Go away",
            denial_handler,
            )(mock_view)
        self._check_enforcement(protected_view, expected_message="Go away",
                                expected_denial_handler=denial_handler)
    
    def _check_enforcement(self, protected_view, expected_message=None,
                           expected_denial_handler=None):
        """Make sure ``predicate`` is not met and enforced as expected."""
        try:
            protected_view(self.req)
        except _AuthorizationDenial, authz_denial:
            eq_(authz_denial.reason, expected_message)
            eq_(authz_denial.handler, expected_denial_handler)
        else:
            raise AssertionError("Authorization denial not raised")


class TestCanAccess(object):
    """Tests for the can_access() function."""
    
    def setUp(self):
        # Let's set up the environment for this mock request:
        mw = RepozeWhatMiddleware()
        self.request = Request({'PATH_INFO': "/"}, make_user(None))
        mw.process_request(self.request)
        mw.process_view(self.request, None, None, None)
        # Let's enabled logging after the middleware has been set:
        self.log_fixture = LoggingHandlerFixture()
    
    def tearDown(self):
        self.log_fixture.undo()
    
    def test_no_authz_decision_made(self):
        """Authorization would be granted if no decision was made."""
        ok_(can_access("/app2/nothing", self.request))
        eq_(len(self.log_fixture.handler.messages['debug']), 1)
        eq_(self.log_fixture.handler.messages['debug'][0],
            "Authorization would be granted on ingress to %s at /app2/nothing" %
            repr(self.request.user))
    
    def test_authz_granted(self):
        """Authorization would be granted if it's granted!."""
        ok_(can_access("/app1/blog", self.request))
        eq_(len(self.log_fixture.handler.messages['debug']), 1)
        eq_(self.log_fixture.handler.messages['debug'][0],
            "Authorization would be granted on ingress to %s at /app1/blog" %
            repr(self.request.user))
    
    def test_authz_denied(self):
        """Authorization would be denied if it's denied!."""
        assert_false(can_access("/app1/admin", self.request))
        eq_(len(self.log_fixture.handler.messages['debug']), 1)
        eq_(self.log_fixture.handler.messages['debug'][0],
            "Authorization would be denied on ingress to %s at /app1/admin" %
            repr(self.request.user))
    
    def test_non_existing_path(self):
        """
        Django's Resolver404 exception must be raised if the path doesn't exist.
        
        """
        assert_raises(Resolver404, can_access, "/app1/non-existing",
                      self.request)


#{ Mock objects


def mock_view(request):
    return "Got it"


#}

