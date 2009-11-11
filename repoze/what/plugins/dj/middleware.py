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
Django middleware for :mod:`repoze.what`.

"""

from logging import getLogger

from django.conf import settings
from django.utils.importlib import import_module

from repoze.what.middleware import setup_request
from repoze.what.acl import ACLCollection

from repoze.what.plugins.dj.denial_handlers import default_denial_handler
from repoze.what.plugins.dj.utils import _AuthorizationDenial

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
            self.acl_collection = settings.GLOBAL_ACL_COLLECTION
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
    
    def process_request(self, request):
        """
        Define the repoze.what credentials.
        
        This is nasty and shouldn't be necessary, but:
        
        - In Django, it's not possible to put WSGI middleware in between
          the core of the Django app and the basic middleware provided by
          Django. To be precise, we'd need to place the :mod:`repoze.what`
          middleware in between Django's authentication routine and the Django
          application/view.
        - We are not going to write so-called "repoze.what source adapters"
          to retrieve the groups and permissions because we can use the user
          object in the request. In the future we might write them to take
          advantage of the other benefits (See:
          `http://what.repoze.org/docs/1.x/Manual/ManagingSources.html`_).
        
        """
        new_environ = setup_request(request.environ, request.user.username,
                                    None, None).environ
        groups = set([g.name for g in request.user.groups])
        permissions = set(request.user.get_all_permissions())
        new_environ['repoze.what.credentials']['groups'] = groups
        new_environ['repoze.what.credentials']['permissions'] = permissions
        # Finally, let's update the Django environ:
        request.environ = new_environ
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check if authorization should be granted for this request or reject
        access if not.
        
        This will also update the :mod:`repoze.what`'s ``named_args`` and
        ``positional_args`` keys in the WGSI environment.
        
        """
        authz_decision = self.acl_collection.decide_authorization(request.environ,
                                                                  view_func)
        if authz_decision is None:
            _LOGGER.info("No authorization decision made on ingress at %s",
                         request.environ['PATH_INFO'])
        elif authz_decision.allow:
            _LOGGER.info("Authorization granted to %s on ingress at %s",
                         request.user, request.environ['PATH_INFO'])
        
        if authz_decision is None or authz_decision.allow:
            return
        
        # We have to deny authorization.
        
        _LOGGER.warn(u"Authorization denied on ingress to %s at %s: %s",
                     request.user, request.environ['PATH_INFO'],
                     authz_decision.message)
        
        if authz_decision.denial_handler is None:
            _LOGGER.debug("No custom denial handler defined; using the default "
                          "one")
            authz_decision.denial_handler = default_denial_handler
        
        return authz_decision.denial_handler(request, authz_decision.message)
    
    def process_exception(self, request, exception):
        """
        Run the default denial handler if a :class:`repoze.what` was raised
        within the view.
        
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

