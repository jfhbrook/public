test:
	pytest -vvv

lint:
	flake8 . --exclude='pyxsession/twisted/*.py'
	pyflakes ./pyxsession/twisted/*.py
	shellcheck ./bin/*
