.PHONY: test lint

test:
	python runtests.py

lint:
	flake8 .
