"""
Setup file for the python_qualiter project
```
"""

from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="python_qualiter",
    version="0.33.0-dev0",
    url="https://gitlab.com/rbacovic/python_qualiter",
    description="A modern Click-based CLI tool for running multiple linting tools on Python files with a clean visual output.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Radovan Bacovic",
    author_email="radovan.bacovic@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
