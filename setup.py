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

import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()
version = open(os.path.join(here, "VERSION.txt")).readline().rstrip()

setup(name="repoze.what-django",
      version=version,
      description=("The repoze.what v1 plugin for Django integration"),
      long_description=README,
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Security"
        ],
      keywords="web application wsgi server django authorization repoze",
      author="Gustavo Narea",
      author_email="repoze-dev@lists.repoze.org",
      namespace_packages = ["repoze", "repoze.what", "repoze.what.plugins"],
      url="http://what.repoze.org/docs/plugins/django/",
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=[
          "repoze.what >= 1.1.0-dev",
          "coverage",
          "nose",
          "Django >= 1.1",
          ],
      install_requires=[
          "repoze.what >= 1.1.0-dev",
          # Django should be installed by hand so the patch should be applied:
          # http://what.repoze.org/docs/plugins/django/install.html
          #"Django >= 1.1",
          "decorator >= 3.0",
          ],
      test_suite="nose.collector",
      entry_points = """\
      """
      )
