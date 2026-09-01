check:
	uv run --no-sync ruff check
	uv run --no-sync ruff format --check
	uv run --no-sync ty check
	uv run --no-sync pytest

fix:
	uv run --no-sync ruff check --fix
	uv run --no-sync ruff format
