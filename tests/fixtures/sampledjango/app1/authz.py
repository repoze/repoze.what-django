# -*- coding: utf-8 -*-
"""
Authorization controls for the mock App 1.

"""

from repoze.what.acl import ACL


def telltale_denial_handler(request, ace_code):
    return "No! Code is %s" % ace_code


control = ACL("/app1")

control.allow("/blog")

control.deny(
    "/admin",
    denial_handler=telltale_denial_handler,
    msg="Get out!",
    code="red",
    )

control.allow("/admin/system-status", code="unrestricted-area")
