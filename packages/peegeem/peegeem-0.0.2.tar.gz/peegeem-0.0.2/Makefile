.PHONY: build clean install pypi docs

build:
	python nbs/build.py

clean:
	rm -rf nbs/__pycache__

work:
	uv run marimo edit nbs/__init__.py

install:
	uv pip install -e . pytest marimo

pypi: clean build
	uv build
	uv publish

docs:
	uvx marimo export html-wasm -o docs nbs/__init__.py
