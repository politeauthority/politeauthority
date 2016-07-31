#!/usr/bin/env python
from distutils.core import setup
import politeauthority
import subprocess

vers = subprocess.check_output([
    "git",
    "rev-list",
    "HEAD",
    "--count"
])

setup(
    name='Polite Authority',
    version='0.0.%s' % vers,
    description='Random Tool Box.',
    author="""
    Alix Fullerton <alix@politeauthority.com>,
    """,
    author_email='alix@politeauthority.com',
    packages=[
        'politeauthority',
    ]
)
