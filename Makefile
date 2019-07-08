test:
	pytest -vvv

lint:
	flake8 . --exclude='korbenware/twisted/*.py'
	pyflakes ./korbenware/twisted/*.py
	shellcheck ./bin/*
