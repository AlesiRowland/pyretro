type-check:
	poetry run mypy . --explicit-package-bases

test:
	poetry run pytest tests --cov src

