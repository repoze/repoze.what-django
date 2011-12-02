# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2009-2011, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
Default denial handler implementations.

"""

from django.http import HttpResponse

__all__ = ("default_denial_handler", )


def default_denial_handler(request, ace_code):
    """
    Return a ``401``/``403`` response depending on whether the user is
    authenticated.
    
    :param request: The Django request object
    :type request: :class:`django.http.HttpRequest`
    :param ace_code: The code associated to the matching ACE
    :return: The Django response
    :rtype: :class:`django.http.HttpResponse`
    
    This will return a ``401`` response if the user is anonymous or ``403`` if
    the user is authenticated.
    
    Strictly speaking, a ``401`` status must come along a ``WWW-Authenticate``
    header, but because we are only dealing with authorization, we are not going
    to do it -- It's up to the authentication routine to challenge the user
    however it wants, even replacing the ``401`` status code with something else.
    
    """
    if request.user.is_authenticated():
        status = 403
    else:
        status = 401
    
    return HttpResponse(status=status)

