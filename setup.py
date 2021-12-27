#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Michael Karamuth",
    author_email="michael@confuzeus.com",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
    ],
    description="{{ cookiecutter.project_short_description }}",
    install_requires=["requests"],
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="django-allcaptcha",
    name="django-allcaptcha",
    packages=find_packages(include=["allcaptcha"]),
    url="https://github.com/confuzeus/django-allcaptcha",
    version="0.1.0",
    zip_safe=False,
)
