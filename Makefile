.PHONY: setup format lint typecheck imports check

setup:
	uv sync

format:
	ruff format .
	black .

lint:
	ruff check .

typecheck:
	mypy qamp

imports:
	python -c "import qamp; print('ok')"

check: lint typecheck imports
