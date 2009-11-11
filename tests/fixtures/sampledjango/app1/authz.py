# -*- coding: utf-8 -*-
"""
Authorization controls for the mock App 1.

"""

from repoze.what.acl import ACL

silly_denial_handler = lambda request, denial_reason: "No! %s" % denial_reason

control = ACL("/app1")
control.allow("/blog")
control.deny("/admin", denial_handler=silly_denial_handler, msg="Get out!")
