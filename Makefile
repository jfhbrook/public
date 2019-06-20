docs: README.ipynb
	jupyter nbconvert --to rst README.ipynb

package:
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

lint:
	flake8 ./twisted_ipython/*.py setup.py

clean:
	rm -rf build
