PYTHON?=python
SOURCES=regen.py regen-git.py test_skel.py

.PHONY: venv
venv: setup
	@echo 'run `source .venv/bin/activate` to use virtualenv'

.PHONY: setup
setup:
	uv sync --group dev

.PHONY: test
test:
	uv run pytest $(TESTOPTS)

.PHONY: format
format:
	uv run ruff format
	uv run ruff check --fix

.PHONY: lint
lint:
	uv run ruff check $(SOURCES)
	uv run mypy --strict $(SOURCES)

.PHONY: checkdeps
checkdeps:
	uv run python -m checkdeps . --allow-names regen
