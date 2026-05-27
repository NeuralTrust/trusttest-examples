UV_AUTH_ENV := UV_INDEX_INTERNAL_USERNAME=oauth2accesstoken UV_KEYRING_PROVIDER=subprocess

.PHONY: install lint

install:
	$(UV_AUTH_ENV) uv tool install keyring --with keyrings.google-artifactregistry-auth
	$(UV_AUTH_ENV) uv sync --all-extras
	uv run pre-commit install --install-hooks

lint:
	uv run ruff check --fix .
	uv run ruff format .
	uv run ty check .
