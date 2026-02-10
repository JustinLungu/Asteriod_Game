# Asteroid Game

A small arcade-style Asteroids clone built with Python and `pygame`.

You control a ship, dodge incoming asteroids, and blast them into smaller pieces.

## Requirements

- Python `3.13+`
- [`uv`](https://docs.astral.sh/uv/) for environment and dependency management

## Quick Start (with uv)

1. Install dependencies:

```bash
uv sync
```

2. Run the game:

```bash
uv run python main.py
```

That command will use the project environment and the pinned dependency from `pyproject.toml` (`pygame==2.6.1`).

## Installing uv (if needed)

If you do not have `uv` yet, install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your shell and run:

```bash
uv --version
```

## Controls

- `W`: move forward
- `S`: move backward
- `A`: rotate left
- `D`: rotate right
- `Space`: shoot
- `Q`: quit game
- `Window close button`: quit game

## Game Notes

- The game runs at about 60 FPS.
- Asteroids spawn from screen edges.
- Large asteroids split into smaller, faster asteroids when shot.
- You lose on collision with any asteroid.

## Logging Output

During a run, the game writes two log files in the project root:

- `game_state.jsonl`: periodic state snapshots
- `game_events.jsonl`: gameplay events (for example, asteroid split or player hit)

These logs are overwritten at the start of each new run.

## Project Structure

- `main.py`: game loop and sprite group wiring
- `player.py`: ship movement, rotation, and shooting
- `asteroid.py`: asteroid rendering, movement, and split behavior
- `asteroidfield.py`: asteroid spawning logic
- `shot.py`: bullet behavior
- `constants.py`: tunable gameplay values
- `logger.py`: JSONL state/event logging
