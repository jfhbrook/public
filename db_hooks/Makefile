SHELL=/bin/bash

install_into_environment:
	pip install -e .

install_kernel:
	python -m ipykernel install --user --name db_hooks

format:
	black .

lint:
	flake8 .

clear:
	rm -rf build
	rm -rf dist

package:
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*
