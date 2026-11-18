# Convenience targets for machines that have `make`. Each one calls the same
# script the /sync-down and /sync-up slash commands use.
.PHONY: bootstrap sync-down sync-up validate test routing studio

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

# Mission Control: the local dashboard over this repo (web/). Builds the
# frontend if needed (Node 22.12+), serves on 127.0.0.1, opens the browser.
studio:
	uv run --frozen python scripts/start_ui.py
