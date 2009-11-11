# -*- coding: utf-8 -*-
"""
Authorization controls for the mock App 1.

"""

from repoze.what.acl import ACL

__all__ = ()


control = ACL("/app1")
control.allow("/blog")
