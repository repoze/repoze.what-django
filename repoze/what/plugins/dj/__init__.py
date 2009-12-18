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
The :mod:`repoze.what` Django plugin.

"""

# Let's import the stuff we want to make accessible from this namespace:
from repoze.what.plugins.dj.middleware import RepozeWhatMiddleware
from repoze.what.plugins.dj.utils import (is_met, not_met, enforce, require,
                                          can_access)
from repoze.what.plugins.dj.predicates import (IsStaff, IsActive, IsSuperuser,
    IS_STAFF, IS_ACTIVE, IS_SUPERUSER)


__all__ = ("RepozeWhatMiddleware", "is_met", "not_met", "enforce", "require",
           "can_access", "IsStaff", "IsActive", "IsSuperuser", "IS_STAFF",
           "IS_ACTIVE", "IS_SUPERUSER")

