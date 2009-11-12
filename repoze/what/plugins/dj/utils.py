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

from logging import getLogger
from functools import wraps

from webob import Request
from django.conf import settings
from django.core.urlresolvers import RegexURLResolver
from django.utils.decorators import auto_adapt_to_methods

from repoze.what.internals import forge_request


__all__ = ("is_met", "not_met", "enforce", "require", "can_access")


_LOGGER = getLogger(__name__)


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


def require(predicate, msg=None, denial_handler=None):
    """
    Enforce ``predicate`` before running a view.
    
    :param predicate: The :mod:`repoze.what` predicate to be evaluated.
    :type predicate: :class:`repoze.what.predicates.Predicate`
    :param msg: The message to be displayed to the user if authorization is
        denied.
    :type msg: :class:`basestring`
    :param denial_handler: The denial handler to be used if authorization is
        denied.
    
    This is a decorator for Django views, so you can be sure that it's safe
    to proceed with the view.
    
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            enforce(predicate, request, msg, denial_handler)
            return view_func(request, *args, **kwargs)
        return wraps(view_func)(_wrapped_view)
    return auto_adapt_to_methods(decorator)


#{ View access verifying functions


def can_access(path, request):
    """
    Forge a request to ``path`` and report whether authorization would be
    granted on ingress.
    
    :param path: The path to another place in the website; it may include the
        query string.
    :type path: :class:`basestring`
    :param request: The Django request to be used as an starting point to forge
        the request.
    :type request: :class:`django.http.HttpRequest`
    :raises django.core.urlresolvers.Resolver404: If ``path`` does not exist.
    
    """
    (view_func, positional_args, named_args) = _get_view_and_args(path, request)
    
    # At this point ``path`` does exist, so it's safe to move on.
    
    authz_control = request.environ['repoze.what.global_control']
    forged_request = forge_request(request.environ, path, positional_args,
                                   named_args)
    
    # Finally, let's verify if authorization would be granted:
    decision = authz_control.decide_authorization(forged_request.environ,
                                                  view_func)
    if decision is None or decision.allow:
        # Authorization would be granted.
        _LOGGER.debug("Authorization would be granted on ingress to %s at %s",
                      request.user, path)
        would_access = True
    else:
        # Authorization would be denied.
        _LOGGER.debug("Authorization would be denied on ingress to %s at %s",
                      request.user, path)
        would_access = False
    
    return would_access


#{ Internal stuff


def _get_view_and_args(path, request):
    """
    Return the view at ``path`` and its named and positional arguments.
    
    Django will raise a Resolver404 exception if ``path`` doesn't exist.
    
    """
    # Let's use urlconf from request object, if available:
    urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
    resolver = RegexURLResolver(r"^/", urlconf)
    return resolver.resolve(path)


#}
