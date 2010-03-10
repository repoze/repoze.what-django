# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009-2010, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
Django middleware for :mod:`repoze.what`.

"""

from logging import getLogger

from django.conf import settings
from django.utils.importlib import import_module

from repoze.what.middleware import setup_request
from repoze.what.acl import ACLCollection

from repoze.what.plugins.dj.denial_handlers import default_denial_handler
from repoze.what.plugins.dj.utils import _AuthorizationDenial
from repoze.what.plugins.dj._utils import resolve_object

__all__ = ("RepozeWhatMiddleware", )


_LOGGER = getLogger(__name__)


class RepozeWhatMiddleware(object):
    """
    Django middleware to support :mod:`repoze.what`-powered authorization.
    
    """
    
    def __init__(self):
        """
        Set the global ACL collection and attach the application-specific
        authorization controls to it.
        
        If there's an ACL collection set in the ``GLOBAL_ACL_COLLECTION``
        setting, then use it instead.
        
        """
        # If there's no global ACL collection, create one:
        if hasattr(settings, "GLOBAL_ACL_COLLECTION"):
            self.acl_collection = resolve_object(settings.GLOBAL_ACL_COLLECTION)
        else:
            self.acl_collection = ACLCollection()
        
        # Let's get the authorization controls for every Django application:
        secured_apps = []
        for app in settings.INSTALLED_APPS:
            authz_module_name = "%s.authz" % app
            try:
                authz_module = import_module(authz_module_name)
            except ImportError:
                continue
            if not hasattr(authz_module, "control"):
                continue
            self.acl_collection.add_acl(authz_module.control)
            secured_apps.append(app)
        
        if secured_apps:
            secured_apps = ", ".join(secured_apps)
            _LOGGER.info("The following applications are secured: %s",
                         secured_apps)
        else:
            _LOGGER.warn("No application is secured")
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check if authorization should be granted for this request or reject
        access if not.
        
        Authorization will be granted if either:
        
        - it was explicitly granted according to the global ACL collection.
        - no decision was made by the global ACL collection.
        
        It will only be denied if authorization was explicitly denied by the
        global ACL collection.
        
        Whatever happens will be logged every time. Denials will be logged as
        warnings and the rest as informational logs.
        
        It does nothing when requested media files.
        
        """
        if (request.path.startswith(settings.MEDIA_URL) or
            request.path.startswith(settings.ADMIN_MEDIA_PREFIX)):
            _LOGGER.debug("Authorization checks disabled for media file at %s",
                          request.environ['PATH_INFO'])
            return
        
        # Letting repoze.what set up the environment:
        if request.user.is_authenticated():
            username = request.user.username
        else:
            username = None
        setup_request(request.environ, username, None, None, self.acl_collection)
        
        # Deciding authorization:
        
        authz_decision = self.acl_collection.decide_authorization(request.environ,
                                                                  view_func)
        if authz_decision is None:
            _LOGGER.debug("No authorization decision made on ingress at %s",
                          request.environ['PATH_INFO'])
        elif authz_decision.allow:
            _LOGGER.info("Authorization granted to %s on ingress at %s",
                         request.user, request.environ['PATH_INFO'])
        
        if authz_decision is None or authz_decision.allow:
            return
        
        # We have to deny authorization.
        
        _LOGGER.warn(u"Authorization denied on ingress to %s at %s: %s",
                     request.user, request.environ['PATH_INFO'],
                     authz_decision.reason)
        
        if authz_decision.denial_handler is None:
            _LOGGER.debug("No custom denial handler defined; using the default "
                          "one")
            authz_decision.denial_handler = default_denial_handler
        
        return authz_decision.denial_handler(request, authz_decision.reason)
    
    def process_exception(self, request, exception):
        """
        Generate a proper response if authorization was denied in the view.
        
        Both :func:`@require <repoze.what.plugins.dj.require>` and
        :func:`enforce <repoze.what.plugins.dj.enforce>` rely on this.
        
        If no authorization denial handler was explicitly set,
        :func:`repoze.what.plugins.dj.denial_handlers.default_denial_handler`
        will be used.
        
        When authorization is denied, a warning will be logged.
        
        """
        if isinstance(exception, _AuthorizationDenial):
            # Authorization was denied in the view. Let's handle it.
            
            _LOGGER.warn("Authorization denied to %s in the view at %s: %s",
                         request.user, request.environ['PATH_INFO'],
                         exception.reason)
            
            if exception.handler is None:
                _LOGGER.debug("Using the default denial handler")
                exception.handler = default_denial_handler
            
            return exception.handler(request, exception.reason)

