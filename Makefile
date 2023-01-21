install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

type-check:
	poetry run mypy . --explicit-package-bases

test:
	poetry run pytest tests --cov src

install: install-poetry
	poetry install
