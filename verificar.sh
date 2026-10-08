#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

uv sync --frozen
uv run python -m compileall -q .
uv run python -c "from main import app; assert app.title == 'Tienda'"
uv run pytest -q
