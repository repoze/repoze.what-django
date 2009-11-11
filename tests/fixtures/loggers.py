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
Test fixtures for the loggers.

"""

import logging

__all__ = ("LoggingHandlerFixture", )


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected log entries."""
    
    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())
    
    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }


class LoggingHandlerFixture(object):
    """Manager of the :class:`MockLoggingHandler`s."""
    
    def __init__(self):
        self.logger = logging.getLogger("repoze.what.plugins.dj")
        self.handler = MockLoggingHandler()
        self.logger.addHandler(self.handler)
    
    def undo(self):
        self.logger.removeHandler(self.handler)

