# -*- coding: utf-8 -*-
"""
Authorization controls for mock app 2.

"""

from repoze.what.acl import ACL

control = ACL("/app2")
control.deny("/secret", reason="This is a secret")
