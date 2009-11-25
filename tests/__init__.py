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
Test suite for the :mod:`repoze.what` Django plugin.

This module only contains mock objects and the like.

"""

import os

from django.core.handlers.wsgi import WSGIRequest
from repoze.what.predicates import Predicate


# Setting the DJANGO_SETTINGS_MODULE variable so the tests can be run:
os.environ['DJANGO_SETTINGS_MODULE'] = "tests.fixtures.sampledjango.settings"


def make_user(username, groups=(), permissions=()):
    """
    Return a mock Django user object.
    
    If ``username`` is ``None``, the user will not be authenticated (i.e.,
    anonymous) and it will have no groups and permissions.
    
    """
    if username:
        group_objects = []
        for group_name in groups:
            group_objects.append(Group(group_name))
        user = User(username, group_objects, permissions)
    else:
        user = AnonymousUser()
    return user


class Request(WSGIRequest):
    """
    Mock Django request.
    
    """
    
    def __init__(self, environ, user):
        # Including the missing items in the WSGI environ:
        full_environ = {
            'REQUEST_METHOD': "GET",
            'SERVER_NAME': "example.org",
            }
        if user.is_authenticated():
            full_environ['REMOTE_USER'] = user.username
        full_environ.update(environ)
        # We're done, let's save it:
        super(Request, self).__init__(full_environ)
        self.user = user


#{ Mock Django models


class User(object):
    def __init__(self, username, groups, permissions):
        self.username = username
        self.groups = GroupSet(groups)
        self.permissions = permissions
        self.message_set = MockMessageSet()
    
    def get_group_permissions(self):
        return ()
    
    def get_all_permissions(self):
        return self.permissions
    
    def is_authenticated(self):
        return True


class AnonymousUser(User):
    
    def __init__(self):
        super(AnonymousUser, self).__init__(None, (), ())
    
    def is_authenticated(self):
        return False


class Group(object):
    
    def __init__(self, name):
        self.name = name


class GroupSet(object):
    def __init__(self, groups):
        self.groups = groups
    
    def all(self):
        return self.groups


#}


class MockMessageSet(object):
    def __init__(self):
        self.messages = []
    
    def create(self, msg):
        self.messages.append(msg)


class MockPredicate(Predicate):
    message = "Mock predicate"
    
    def __init__(self, result=True, *args, **kwargs):
        self.result = result
        super(MockPredicate, self).__init__(*args, **kwargs)
    
    def evaluate(self, environ, credentials):
        if not self.result:
            self.unmet()
