# search/setup.py

import os
from setuptools import setup


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="sefile",
    version="0.0.1",
    author="Faisal Ramadhan",
    author_email="faisalramadhan1299@gmail.com",
    description=("CLI tool for searching your file in your PC"),
    license="GPLv3",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)"
    ],
    url="https://github.com/Kolong-Meja/search-cli",
    entry_points="""
        [console_scripts]
        sefile=search.app:main
        """,
)