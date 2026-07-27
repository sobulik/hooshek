check:
	uv run ruff check
	uv run ruff format --check
	uv run ty check
	uv run pytest

fix:
	uv run ruff check --fix
	uv run ruff format
