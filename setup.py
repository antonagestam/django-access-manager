#!/usr/bin/env python

from setuptools import setup, find_packages
import access

setup(
    name='django-access-tools',
    version=".".join(map(str, access.__version__)),
    author='Anton Agestam',
    author_email="msn@antonagestam.se",
    url='http://antonagestam.github.io/django-access-tools',
    install_requires=[
        'Django>=2.0',
    ],
    description='An abstract access manager for Django.',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
