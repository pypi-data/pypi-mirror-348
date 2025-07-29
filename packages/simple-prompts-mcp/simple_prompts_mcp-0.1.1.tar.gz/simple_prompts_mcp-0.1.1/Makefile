SHELL = /usr/bin/env bash -xeuo pipefail

format:
	uv run ruff check --select I --fix src/
	uv run ruff format src/

.PHONY: \
	format
