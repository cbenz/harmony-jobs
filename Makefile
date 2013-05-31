.PHONY: clean flake8 jshint tests

all: clean flake8 jshint tests

clean:
	find -name "*.pyc" | xargs rm -f
	rm -rf cache/*

flake8:
	flake8 --max-line-length=120 --ignore=E123,E128,E251 harmony_jobs

jshint:
	jshint harmony_jobs/static/js/*.js

tests:
	nosetests
