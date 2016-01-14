.PHONY: test lint test-coverage coveralls

test:
	python runtests.py

lint:
	flake8 .

test-coverage:
	coverage run runtests.py

coveralls:
	coveralls

distribute:
	python setup.py sdist bdist_wheel upload
