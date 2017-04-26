# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re, sys, os, glob
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('nodelistener/nodelistener.py').read(),
    re.M
    ).group(1)


setup(
    name = "idcnodelistener",
    packages = ["nodelistener","recordingclasses"],
    entry_points = {
        "console_scripts": ['startlistener = startlistener:main']
        },
    scripts = ['bin/atclear'],
    version = version,
    description = "Listens for commands from an instance of an idc-controller.",
    author = "Intelligent Digital Communications",
    author_email = "vip-idc@gatech.edu",
    url = "http://github.gatech.edu/IDC/node-infrastructure",
    test_suite="test.schedule_session_tests",
    install_requires=['hug']
)
