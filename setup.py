#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

setup(
    name='vcrwrapper',
    version='0.0.10',
    description=(
        "Wrapper around vcr"
    ),
    author='Antoine Reversat',
    author_email='a.reversat@gmail.com',
    url='https://github.com/crevetor/vcrwrapper',
    packages=find_packages(exclude=("tests*",)),
    install_requires=['vcrpy', 'Django'],
    license='GPLv2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: GPL',
    ]
)
