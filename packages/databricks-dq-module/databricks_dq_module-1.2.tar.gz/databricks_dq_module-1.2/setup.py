from setuptools import setup, find_packages

setup(
    name = "databricks-dq-module",
    version = "1.2",
    packages = find_packages(),
    description = "Data quality checker for Databricks pipelines",
    author = "Noah Kim",
    author_email = "noah24.kim@gmail.com",
    install_requires = [],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires = ">= 3.6"
)