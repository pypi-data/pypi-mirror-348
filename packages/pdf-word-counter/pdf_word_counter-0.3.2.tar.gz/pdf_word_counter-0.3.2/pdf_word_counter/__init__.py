"""
pdf_word_counter
================

A small utility package that counts word occurrences in PDF files and
outputs the results as either an Astropy Table or a pandas DataFrame.

CLI usage is exposed via the ``pdf-word-counter`` console script.
"""
from importlib import metadata as _md

try:
    __version__ = _md.version(__name__)
except _md.PackageNotFoundError:  # running from source/tree
    from .version import __version__  # noqa: F401

