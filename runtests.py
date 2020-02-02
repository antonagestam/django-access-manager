#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from django.conf import settings
from django import setup
from django.test.runner import DiscoverRunner


if __name__ == "__main__":
    settings.configure(
        **{
            "DATABASES": {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": "",
                    "USER": "",
                    "PASSWORD": "",
                }
            },
            "INSTALLED_APPS": (
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "access",
            ),
        }
    )
    setup()
    failures = DiscoverRunner(verbosity=1).run_tests(["access"])
    if failures:
        sys.exit(failures)
