#!/usr/bin/env python3
import os
import sys
from setuptools import setup

setup(
    name="activate",
    version="0.2.1",
    author="Ale & ZeDoCaixao",
    description="Replace libsteam_api.so with an ACTiVATED one",
    long_description=open("README.rst").read(),
    url="https://github.com/notpushkin/activate",
    py_modules=["activate"],
    entry_points="""
        [console_scripts]
        activate=activate:main
    """,
)
