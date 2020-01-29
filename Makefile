# This Makefile is based on the Makefile defined in the Python Best Practices repository:
# https://git.datapunt.amsterdam.nl/Datapunt/python-best-practices/blob/master/dependency_management/

COMPOSE_PROJECT_NAME ?= vlog
dc = docker-compose -p $(COMPOSE_PROJECT_NAME)
testcommand = $(dc) run --rm test $(TESTARGS)

help:                                   ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:                                ## Install requirements and sync venv with expected state as defined in requirements.txt
	pip install -r requirements_dev.txt
	pip-sync requirements.txt requirements_dev.txt

requirements:                           ## Upgrade requirements (in requirements.in) to latest versions and compile requirements.txt
	pip-compile --upgrade --output-file requirements.txt requirements.in

upgrade: requirements install           ## Run 'requirements' and 'install' targets

migrations:
	$(dc) run --rm app python manage.py makemigrations

migrate:
	$(dc) run --rm app python manage.py migrate
