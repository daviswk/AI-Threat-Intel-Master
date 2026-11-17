# Convenience targets for machines that have `make`. Each one calls the same
# script the /sync-down and /sync-up slash commands use.
.PHONY: bootstrap sync-down sync-up validate test routing

bootstrap:
	bash scripts/bootstrap_laptop.sh

sync-down:
	bash scripts/sync_down.sh

sync-up:
	bash scripts/sync_up.sh

validate:
	uv run --frozen python scripts/validate_state.py
	uv run --frozen python scripts/check_portable.py

test:
	uv run --frozen python -m pytest assurance-harness

routing:
	uv run --frozen python scripts/verify_routing.py
