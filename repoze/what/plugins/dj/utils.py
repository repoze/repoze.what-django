# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009-2011, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
In-view utilities for the :mod:`repoze.what` Django plugin.

"""

from logging import getLogger
from functools import wraps

from webob import Request
from django.conf import settings
from django.core.urlresolvers import RegexURLResolver

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
    
    This function is intented to help you get finer grained control on what
    is authorized. If you are controlling access to the whole view, this
    function is not the right one: Use :func:`@require
    <repoze.what.plugins.dj.require` or :func:`enforce
    <repoze.what.plugins.dj.enforce>` instead.
    
    Sample use::
    
        from django.http import HttpResponse
        
        from repoze.what.plugins.dj import is_met
        from repoze.what.predicates import not_anonymous
        from repoze.what.plugins.ip import ip_from
        
        def my_view(request):
            if is_met(not_anonymous() & ip_from(["127.0.0.1", "192.168.1.0/24"]), request):
                request.user.message_set.create("This is a secret message. "
                                                "Only people on this network "
                                                "can see it.")
            return HttpResponse("Hi there!")
    
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
    
    This function is intented to help you get finer grained control on what
    is authorized. If you are controlling access to the whole view, this
    function is not the right one: Use :func:`@require
    <repoze.what.plugins.dj.require` or :func:`enforce
    <repoze.what.plugins.dj.enforce>` instead.
    
    Sample use::
    
        from django.http import HttpResponse
        
        from repoze.what.plugins.dj import not_met
        from repoze.what.predicates import not_anonymous
        from repoze.what.plugins.ip import ip_from
        
        def my_view(request):
            rights = ["You can watch TV", "You can eat", "You can jump"]
            if not_met(not_anonymous() & ip_from(["127.0.0.1", "192.168.1.0/24"]), request):
                # If the user is not authenticated and within the local network,
                # he cannot watch TV!
                del rights[0]
            return HttpResponse(", ".join(rights))
    
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
    
    Sample use::
    
        from django.http import HttpResponse
        
        from repoze.what.predicates import in_any_group
        from repoze.what.plugins.dj import enforce
        
        def sample_view(request):
            enforce(in_any_group("admins", "dev"))
            return HttpResponse("You're an admin and/or a developer!")
    
    If the user does not belong to the "admins" or "dev" groups, the code
    inside the view will get executed until the ``enforce()`` statement, where
    an exception will be raised and authorization will be denied using the
    default handler.
    
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
    Enforce ``predicate`` **before** running a view.
    
    :param predicate: The :mod:`repoze.what` predicate to be evaluated.
    :type predicate: :class:`repoze.what.predicates.Predicate`
    :param msg: The message to be displayed to the user if authorization is
        denied.
    :type msg: :class:`basestring`
    :param denial_handler: The handler to be used if authorization is denied.
    
    This is a decorator for Django views, so you can be sure that it's safe
    to proceed with the view.
    
    Sample use::
    
        from django.http import HttpResponse
        
        from repoze.what.predicates import in_any_group
        from repoze.what.plugins.dj import require
        
        @require(in_any_group("admins", "dev"))
        def sample_view(request):
            return HttpResponse("You're an admin and/or a developer!")
    
    If the user does not belong to the "admins" or "dev" groups, the code
    inside the view won't get executed and authorization will be denied using
    the default handler.
    
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            enforce(predicate, request, msg, denial_handler)
            return view_func(request, *args, **kwargs)
        return wraps(view_func)(_wrapped_view)
    return decorator


#{ View access verifying functions


def can_access(path, request, view_func=None, view_args=(),
               view_kwargs={}):
    """
    Forge a request to ``path`` and report whether authorization would be
    granted on ingress.
    
    :param path: The path to another place in the website; it may include the
        query string.
    :type path: :class:`basestring`
    :param request: The Django request to be used as an starting point to forge
        the request.
    :type request: :class:`django.http.HttpRequest`
    :param view_func: The Django view at ``path``.
    :param view_args: The positional arguments for ``view_func``.
    :type view_args: :class:`tuple`
    :param view_kwargs: The named arguments for ``view_func``.
    :type view_kwargs: :class:`dict`
    :raises django.core.urlresolvers.Resolver404: If ``path`` does not exist.
    
    If ``view_func`` is not passed, this function will resolve it.
    
    Sample use::
    
        from django.core.urlresolvers import reverse
        from django.http import HttpResponse, HttpResponseRedirect
        
        from repoze.what.plugins.dj import can_access
        
        def take_me_somewhere(request):
            if can_access("/admin/", request):
                # The current user can access the admin site.
                return HttpResponseRedirect("/admin/")
            elif can_access("/blog/posts/16", request):
                # The current user can access blog post #16.
                return HttpResponseRedirect("/blog/post/16")
            
            if not can_access("/", request):
                # The current user cannot access the homepage.
                request.user.message_set.create("You cannot even visit the "
                                                "homepage!")
            
            return HttpResponse("You're staying here in the mean time!")
    
    .. note::
        Only access rules available in the global ACL collection will be taken
        into account. Rules set with :func:`@require
        <repoze.what.plugins.dj.require` or :func:`enforce
        <repoze.what.plugins.dj.enforce>` cannot be taken into account.
    
    """
    if not view_func:
        # The view is not passed; we have to find it!
        (view_func, view_args, view_kwargs) = _get_view_and_args(path, request)
    
    # The arguments may be None:
    view_args = view_args or ()
    view_kwargs = view_kwargs or {}
    
    # At this point ``path`` does exist, so it's safe to move on.
    
    authz_control = request.environ['repoze.what.global_control']
    forged_request = forge_request(request.environ, path, view_args,
                                   view_kwargs)
    
    # While deciding authorization, the predicates evaluated may depend on
    # the request having a specific status as in real requests, which is
    # solved by running the appropriate Django middleware:
    for django_view_middleware in request.environ['repoze.what.dj_view_mw']:
        response = django_view_middleware.process_view(
            forged_request,
            view_func,
            view_args,
            view_kwargs,
            )
        
        if response:
            _LOGGER.debug(
                "Authorization would be denied on ingress to %s at %s by the "
                "middleware %s",
                request.user,
                path,
                django_view_middleware.__class__.__name__,
                )
            return False
    
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
