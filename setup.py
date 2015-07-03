#!/usr/bin/env python

from setuptools import setup, find_packages
import access

setup(
    name='django-access-tools',
    version=".".join(map(str, access.__version__)),
    author='Anton Agestam',
    author_email="msn@antonagestam.se",
    url='http://github.com/antonagestam/django-access-tools',
    install_requires=[
        'Django>=1.8.2',
    ],
    description='An abstract access manager for Django.',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
)
