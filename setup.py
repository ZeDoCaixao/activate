#!/usr/bin/env python3
import os
import sys
from setuptools import setup

setup(
    name="activate",
    version="0.1.0",
    author="ZeDoCaixao",
    description="Replace libsteam_api.so with an ACTiVATED one",
    url="https://github.com/ZeDoCaixao/activate",
    py_modules=["activate"],
    entry_points="""
        [console_scripts]
        activate=activate:main
    """,
)
