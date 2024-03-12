# !/usr/bin/env python
# This file was written based on GitHub user @iann838's approach on the subject

import sys

from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

# Require Python 3.11
if sys.version_info.major != 3 and sys.version_info.minor < 11:
    sys.exit("Module 'voidsafe' requires Python >= 3.11")

setup(
    name = "voidsafe",
    version = "0.1.0",
    author = "Gustavo Cardoso Ribeiro",
    author_email = "gustavocaribe@caribesphaneron.com",
    url = "https://github.com/gus-caribe/voidsafe",
    description = "A void-safe, None-aware approach at Python programming language.",
    long_description = "",
    long_description_content_type = 'text/markdown',
    keywords = ["voidsafe", "nullsafe", "none-aware", "python"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.11",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    license = "MIT",
    packages = find_packages(exclude = ("test")),
    zip_safe = True,
    install_requires = [],
    include_package_data = True,
)