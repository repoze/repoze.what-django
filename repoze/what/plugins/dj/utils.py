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
In-view utilities for the :mod:`repoze.what` Django plugin.

"""

__all__ = ("is_met", "not_met", "enforce", "can_access", "can_access_reverse")


#{ Predicate evaluation functions


def is_met(predicate, request):
    """
    Report whether ``predicate`` is met in the ``request``.
    
    :param predicate: The :mod:`repoze.what` predicate to be evaluated.
    :type predicate: :class:`repoze.what.predicates.Predicate`
    :param request: The Django request object.
    :type request: :class:`django.http.HttpRequest`
    :return: Whether the ``predicate`` is met.
    :rtype: :class:`bool`
    
    """
    return predicate.is_met(request.environ)


def not_met(predicate, request):
    """
    Report whether ``predicate`` is **not** met in the ``request``.
    
    :param predicate: The :mod:`repoze.what` predicate to be evaluated.
    :type predicate: :class:`repoze.what.predicates.Predicate`
    :param request: The Django request object.
    :type request: :class:`django.http.HttpRequest`
    :return: Whether the ``predicate`` is **not** met.
    :rtype: :class:`bool`
    
    """
    return not is_met(predicate, request)


def enforce(predicate, request, msg=None, denial_handler=None):
    """
    Stop here if ``predicate`` is not met within the ``request``.
    
    :param predicate: The :mod:`repoze.what` predicate to be evaluated.
    :type predicate: :class:`repoze.what.predicates.Predicate`
    :param request: The Django request object.
    :type request: :class:`django.http.HttpRequest`
    :param msg: The message to be displayed to the user if authorization is
        denied.
    :type msg: :class:`basestring`
    :param denial_handler: The denial handler to be used if authorization is
        denied.
    :raises _AuthorizationDenial: If the ``predicate`` is not met.
    
    """
    if not_met(predicate, request):
        denial = _AuthorizationDenial(msg, denial_handler)
        raise denial


class _AuthorizationDenial(Exception):
    """
    Authorization denial.
    
    These objects are raised from the view, but they **are not exceptions**
    strictly speaking: Exceptions represent errors, and an unmet predicate is
    not an error. That's why this class is internal and does not end with
    "Error"/"Exception".
    
    This is intented to be used only by :func:`enforce` and
    :class:`repoze.what.plugins.dj.RepozeWhatMiddleware`.
    
    """
    
    def __init__(self, reason, handler):
        self.reason = reason
        self.handler = handler


#{ View access verifying functions


def can_access(path, request):
    pass


def can_access_reverse(path, request, *args, **kwargs):
    pass


#}
