# -*- coding: utf-8 -*-
"""
Django middleware.

"""


class AddEnvironItem(object):
    """Useless middleware to add an item to the WSGI environ."""
    
    def process_view(self, request, view, view_args, view_kwargs):
        request.environ['foo'] = "baz"
