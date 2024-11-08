.PHONY: init format check requirements

init:
	python -m pip install -q -U poetry ruff isort
	python -m poetry install

format:
	ruff format code_search

check:
	ruff check code_search

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export -f requirements.txt --output requirements-dev.txt --without-hashes --with dev