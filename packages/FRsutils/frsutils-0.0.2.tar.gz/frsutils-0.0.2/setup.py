# setup.py
from setuptools import setup, find_packages

setup(
    name="FRsutils",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
    ],
    author="Mehran Amiri",
    author_email='meam64@gmail.com',
    description="A Python library for fuzzy-rough set utility functions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mehi64/FRsutils",
    license="AGPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
