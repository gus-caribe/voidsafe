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
    version = "0.2.0",
    author = "Gustavo Cardoso Ribeiro",
    author_email = "gustavocaribe@caribesphaneron.com",
    url = "https://github.com/gus-caribe/voidsafe",
    description = "A null-safe-like approach to Python programming language.",
    long_description = """
        `VoidSafe` is a package that brings a '_null-safe-like_' approach to Python3-written 
        scripts and applications. It provides software developers with resources to apply 
        `void-safety` principles to their codebase, allowing `safe` operations to be performed 
        on `Potentially Unsafe Instances [2.1]` , which helps assuring that your software will 
        be able to handle many `memory-access` problems at runtime.
    """,
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