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
    description="Easily integrate captcha services in your Django project.",
    install_requires=["requests"],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="django-allcaptcha",
    name="django-allcaptcha",
    packages=find_packages(include=["allcaptcha", "allcaptcha.*"]),
    url="https://github.com/confuzeus/django-allcaptcha",
    version="0.3.0",
    zip_safe=False,
)
