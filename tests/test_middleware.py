# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
Tests for the Django middleware for :mod:`repoze.what`.

"""

from nose.tools import eq_, ok_

from repoze.what.plugins.dj import RepozeWhatMiddleware

from tests import Request, make_user
from tests.fixtures.loggers import LoggingHandlerFixture


class TestAuthzDiscovery(object):
    """Tests to check whether the authorization controls are found correctly."""
    
    def setUp(self):
        self.log_fixture = LoggingHandlerFixture()
    
    def tearDown(self):
        self.log_fixture.undo()
    
    def test_global_acl_collection_and_secured_apps(self):
        mw = RepozeWhatMiddleware()
        # Checking that the global ACL collection was pciked:
        from tests.fixtures.sampledjango.settings import GLOBAL_ACL_COLLECTION
        eq_(GLOBAL_ACL_COLLECTION, mw.acl_collection)
        # Checking that the app-specific controls were picked:
        from tests.fixtures.sampledjango.app1.authz import control as control1
        from tests.fixtures.sampledjango.app2.authz import control as control2
        ok_(control1 in mw.acl_collection._acls)
        ok_(control2 in mw.acl_collection._acls)
        # Checking the logs:
        eq_(len(self.log_fixture.handler.messages['info']), 1)
        eq_(self.log_fixture.handler.messages['info'][0], 
            ("The following applications are secured: "
             "tests.fixtures.sampledjango.app1, "
             "tests.fixtures.sampledjango.app2")
            )


class TestCredentials(object):
    """
    Tests to make sure the repoze.what credentials are set properly.
    
    """
    
    def setUp(self):
        self.middleware = RepozeWhatMiddleware()
    
    def test_anonymous_user(self):
        """Anonymous users shouldn't have groups nor permissions."""
        environ = {}
        request = Request(environ, make_user(None))
        # Running the middleware and checking the resulting environ:
        self.middleware.process_request(request)
        eq_(len(request.environ['repoze.what.credentials']['groups']), 0)
        eq_(len(request.environ['repoze.what.credentials']['permissions']), 0)
        eq_(request.environ['repoze.what.credentials']["repoze.what.userid"],
            None)
    
    def test_user_with_groups_and_no_permissions(self):
        environ = {}
        request = Request(environ, make_user("foo", ("g1", "g2", "g3")))
        # Running the middleware and checking the resulting environ:
        self.middleware.process_request(request)
        eq_(request.environ['repoze.what.credentials']['groups'],
            set(["g1", "g2", "g3"]))
        eq_(len(request.environ['repoze.what.credentials']['permissions']), 0)
        eq_(request.environ['repoze.what.credentials']['repoze.what.userid'],
            "foo")
    
    def test_user_with_permissions_and_no_groups(self):
        environ = {}
        request = Request(environ, make_user("foo", [], ("p1", "p2", "p3")))
        # Running the middleware and checking the resulting environ:
        self.middleware.process_request(request)
        eq_(len(request.environ['repoze.what.credentials']['groups']), 0)
        eq_(request.environ['repoze.what.credentials']['permissions'],
            set(["p1", "p2", "p3"]))
        eq_(request.environ['repoze.what.credentials']['repoze.what.userid'],
            "foo")
    
    def test_no_response_returned(self):
        """The middleware's process_request() shouldn't return a response."""
        request = Request({}, make_user(None))
        eq_(self.middleware.process_request(request), None)



