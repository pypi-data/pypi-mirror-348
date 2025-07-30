"""Importing Path"""
from pathlib import Path
import setuptools
setuptools.setup(
    name="sunandmoonpdf",
    version='1.0.3',
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"])
)
