default:
    just --list

init:
    uv sync --all-extras
    uv run pre-commit install

pre-commit:
    uv run pre-commit run --all-files

lint:
    uv run ruff format
    uv run ruff check --fix || true
    uv run mypy .

tests *options="":
    uv run pytest {{ options }}
