# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
Unit tests for the miscellaneous utilities at
:mod:`repoze.what.plugins.dj._.utils`.

"""

from nose.tools import eq_, assert_raises

from repoze.what.plugins.dj._utils import resolve_object

from tests.fixtures.misc_objects import my_object


FIXTURES_MODULE = "tests.fixtures.misc_objects."


class TestResolveObject(object):
    """Tests for :func:`resolve_object`."""
    
    def test_non_existing_module(self):
        assert_raises(ValueError, resolve_object, "non_existing_module.object")
    
    def test_non_existing_object(self):
        assert_raises(ValueError, resolve_object,
                      FIXTURES_MODULE + "non_existing_object")
    
    def test_getting_object(self):
        object_ = resolve_object(FIXTURES_MODULE + "my_object")
        eq_(object_, my_object)
    
    def test_getting_none_object(self):
        object_ = resolve_object(FIXTURES_MODULE + "my_none")
        eq_(object_, None)
