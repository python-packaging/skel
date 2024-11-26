PYTHON?=python
SOURCES=regen.py regen-git.py

UV:=$(shell uv --version)
ifdef UV
	VENV:=uv venv
	PIP:=uv pip
else
	VENV:=python -m venv
	PIP:=python -m pip
endif

.PHONY: venv
venv:
	$(VENV) .venv
	source .venv/bin/activate && make setup
	@echo 'run `source .venv/bin/activate` to use virtualenv'

# The rest of these are intended to be run within the venv, where python points
# to whatever was used to set up the venv.

.PHONY: setup
setup:
	$(PIP) install -Ur requirements-dev.txt

.PHONY: format
format:
	ruff format
	ruff check --fix

.PHONY: lint
lint:
	ruff check $(SOURCES)
	mypy --strict $(SOURCES)

.PHONY: checkdeps
checkdeps:
	python -m checkdeps . --allow-names regen
