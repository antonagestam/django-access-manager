.PHONY: test

test:
	export PYTHONPATH=`pwd`; runtests.py --settings='test_settings'
