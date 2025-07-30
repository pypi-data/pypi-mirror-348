# byte_sleuth package
# -*- coding: utf-8 -*-
"""
byte_sleuth package
==================
A package for scanning files and directories for suspicious ASCII control and Unicode characters, with optional sanitization and backup features.

Provides the ByteSleuth class for use as a library or via CLI, enabling detection and removal of control characters from text files. Designed for international use and follows Python packaging best practices.
"""
from .byte_sleuth import ByteSleuth

__all__ = [
    "ByteSleuth"
]

__version__ = "1.0.2"
__author__ = "Rafael Mori"
__email__ = "faelmori@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024 Rafael Mori"
__status__ = "Development"
__url__ = "https://github.com/rafaelmori/byte_sleuth"
__description__ = (
    "A package for scanning and sanitizing files for suspicious ASCII and Unicode characters."
)
__keywords__ = [
    "byte scan",
    "unicode",
    "ascii",
    "sanitization",
    "file integrity",
    "security",
    "data cleaning",
]
__install_requires__ = [
    "rich>=13.3.5",
    "pytest",
    "flake8"
]
__extras_require__ = {
    "dev": [
        "pytest",
        "black",
        "flake8",
        "mypy",
        "isort",
        "pre-commit",
        "pandas",  # If used in future for reporting or batch processing
        "numpy",   # If used in future for performance or array ops
        "matplotlib",  # For possible future visualizations
        "seaborn",     # For possible future visualizations
        "jinja2",      # For possible future templating
    ],
    "docs": [
        "sphinx",
        "sphinx_rtd_theme",
    ],
}
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]