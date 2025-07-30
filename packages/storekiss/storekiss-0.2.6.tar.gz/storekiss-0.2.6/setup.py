"""
storekiss - A CRUD interface library with SQLite storage and FireStore-like API
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="storekiss",
    version="0.2.6",
    author="Taka",
    author_email="tkykszk@gmail.com",
    description="A CRUD interface library with SQLite storage and FireStore-like API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tkykszk/storekiss",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
