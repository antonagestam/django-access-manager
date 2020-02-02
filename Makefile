.PHONY: test lint test-coverage coveralls install-test-requirements distribute
SHELL := /usr/bin/env bash

test:
	python3 runtests.py

install-test-requirements:
	python3 -m pip install -e .[test]

lint:
	flake8 .
	black --check .

test-coverage:
	coverage run runtests.py

coveralls:
	coveralls

clean:
	rm -rf django_access_tools.egg-info __pycache__ build dist

build: clean
	python3 -m pip install --upgrade wheel twine setuptools
	python3 setup.py sdist bdist_wheel

distribute: build
	python3 -m twine upload dist/*

test-distribute: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
