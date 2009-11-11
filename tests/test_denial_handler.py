# -*- coding: utf-8 -*-
"""
Unit tests suite for the default denial handler implementation.

"""

from nose.tools import eq_

from repoze.what.plugins.dj.denial_handlers import default_denial_handler

from tests import Request, make_user


class TestDenialHandler(object):
    """Tests for the default denial handler."""
    
    def test_user_is_anonymous(self):
        req = Request({}, make_user(None))
        response = default_denial_handler(req, "You can't be here")
        eq_(response.status_code, 401)
        eq_(len(req.user.message_set.messages), 1)
        eq_(req.user.message_set.messages[0], "You can't be here")
    
    def test_user_is_authenticated(self):
        req = Request({}, make_user("Foo"))
        response = default_denial_handler(req, "What are you doing here?")
        eq_(response.status_code, 403)
        eq_(len(req.user.message_set.messages), 1)
        eq_(req.user.message_set.messages[0], "What are you doing here?")
    
    def test_no_message_set(self):
        """No message should be shown to the user if there's none set."""
        req = Request({}, make_user(None))
        response = default_denial_handler(req, None)
        eq_(response.status_code, 401)
        eq_(len(req.user.message_set.messages), 0)
