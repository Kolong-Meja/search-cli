# search/setup.py

import os
from setuptools import setup


def read(filename: str):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="sefile",
    version="0.0.1",
    author="Faisal Ramadhan",
    author_email="faisalramadhan1299@gmail.com",
    description=("CLI tool for searching your file in your PC"),
    license="GPLv3",
    long_description=read("README"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)"
    ],
    entry_points="""
    [console_scripts]
    sefile=search.app:main
    """,
)