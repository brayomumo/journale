install-requirements:
	pip install -r requirements/base.txt

test:
	pip install -r requirements/test.txt
	coverage run manage.py test --verbosity 3
	coverage report

run-dev:
	python manage.py runserver 0.0.0.0:8000