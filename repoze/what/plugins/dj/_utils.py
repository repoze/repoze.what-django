# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
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
Internal utilities for the :mod:`repoze.what` Django plugin.

"""

from django.utils.importlib import import_module


__all__ = ("resolve_object", )


def resolve_object(object_string):
    """
    Resolve ``object_string`` and return the actual object.
    
    :param object_string: The object to be resolved.
    :type object_string: :class:`basestring`
    :return: The object requested.
    :raises ValueError: If there was an problem while importing the module or
        the object (e.g., the object/module does not exist).
    
    For example, you could do::
    
        settings = resolve_object("django.conf.settings")
    
    """
    (module_name, object_name) = object_string.rsplit(".", 1)
    
    try:
        module = import_module(module_name)
    except ImportError, exc:
        raise ValueError("Could not import module %s: %s" % (module_name, exc))
    
    if not hasattr(module, object_name):
        raise ValueError("Module %s does not have object %s" %
                        (module_name, object_name))
    
    return getattr(module, object_name)
