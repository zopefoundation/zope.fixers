##############################################################################
#
# Copyright (c) 2009 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.fixers package
"""
from setuptools import setup, find_packages
import os

setup(name='zope.fixers',
      version='1.1.1',
      description="2to3 fixers for Zope",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",

        ],
      keywords='2to3 python3 zope',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='http://svn.zope.org/zope.fixers/',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zope'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [console_scripts]
      zope-2to3 = zope.fixers.main:main
      """,
      test_suite = 'zope.fixers.tests',
      )
