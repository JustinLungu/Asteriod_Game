#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run python -m asteriod_game.rl.plot "$@"
