.PHONY: test lint test-coverage coveralls install-test-requirements distribute
SHELL := /usr/bin/env bash

test:
	python3 runtests.py

install-test-requirements:
	python3 -m pip install -e .[test]

lint:
	flake8 .

test-coverage:
	coverage run runtests.py

coveralls:
	coveralls

clean:
	rm -rf django_access_tools.egg-info __pycache__ build dist

distribute:
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
