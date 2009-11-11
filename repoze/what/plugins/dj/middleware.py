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

from repoze.what.middleware import setup_request

__all__ = ("RepozeWhatMiddleware", )


class RepozeWhatMiddleware(object):
    """
    Django middleware to support :mod:`repoze.what`-powered authorization.
    
    """
    
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
        pass
    
    def process_exception(self, request, exception):
        pass
