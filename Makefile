.PHONY: clean help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-pyc clean-dist ## Remove all Python artifacts.

clean-pyc: ## Remove file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.coverage' -exec rm -fr {} +
	find . -name 'coverage.xml' -exec rm -fr {} +

clean-dist: ## Clean build artifacts.
	rm -rf build
	rm -rf dist

test: ## Run tests quickly with the default Python.
	pytest

coverage: ## Run tests quickly with the default Python.
	pytest --cov-report xml --cov-report term-missing --cov=event_handler tests --cov-fail-under=100

format: ## Format code following configured styleguide.
	pre-commit run --all

install-pkg: clean ## Install the package to the active Python's site-packages.
	pip install -e .

install-dev: clean ## Install the package for local development.
	[ ! -d .git ] && git init || echo "Git repository already exists"
	pip install --upgrade pip
	pip install -e ".[development]"
	pip install -e ".[dependencies]"
	pre-commit install
	pre-commit autoupdate
	cz init

dump-requirements: ## Dumps dependencies into requirements.txt.
	pip freeze > requirements.txt

check-version: ## Check versions of installed packages.
	pip-licenses --from=mixed --order=license

bumpversion: ## Bump version based on conventional commits.
	cz bump

changelog: ## Generate CHANGELOG.md based on conventional commits.
	cz changelog

run:  ##Runs application
	python3.11 event_handler/main.py
