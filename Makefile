.PHONY: dev format format-fix deps build test-infra test-service test deploy destroy
PYTHON := $(or $(PYTHON_PATH), ".venv/bin/python3")
.ONESHELL:  # run all commands in a single shell, ensuring it runs within a local virtual env

dev:
	poetry config --local virtualenvs.in-project true
	poetry install --no-root --with dev

format:
	poetry run ruff check . --fix

format-fix:
	poetry run ruff format .

deps:
	poetry export --without-hashes --only=dev --format=requirements.txt > dev_requirements.txt
	poetry export --without-hashes --without=dev --format=requirements.txt > lambda_requirements.txt

build:
	mkdir -p .build/lambdas ; cp -r service .build/lambdas
	mkdir -p .build/layers ; poetry export --without=dev --without-hashes --format=requirements.txt > .build/layers/requirements.txt

test-infra: build
	poetry run pytest -l -s --pdb tests/infrastructure

test-service: build
	poetry run pytest -l -s --pdb tests/service

test:
	poetry run pytest -l -s --pdb tests/

deploy: build
	npx cdk deploy --app="${PYTHON} ${PWD}/app.py" --require-approval=never

destroy:
	npx cdk destroy --app="${PYTHON} ${PWD}/app.py" --force
