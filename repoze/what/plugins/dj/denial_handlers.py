# -*- coding: utf-8 -*-
"""


"""

from django.http import HttpResponse

__all__ = ("default_denial_handler")


def default_denial_handler(request, denial_reason):
    """
    Return a 401/403 response and explain the user why authorization was denied.
    
    This will return a 401 status if the user is anonymous or 403 if the user
    is authenticated.
    
    Strictly speaking, a 401 status must come along a ``WWW-Authenticate``
    header, but because we are only dealing with authorization, it's up to the
    authentication routine to challenge the user however it wants -- Even
    replacing the 401 status code with something else.
    
    If a ``denial_reason`` is set, it will be shown to the user.
    
    """
    if request.user.is_authenticated():
        status = 403
    else:
        status = 401
    
    if denial_reason:
        request.user.message_set.create(denial_reason)
    
    return HttpResponse(status=status)

