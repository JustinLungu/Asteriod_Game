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
./scripts/play.sh
```

That command will use the project environment and the pinned dependency from `pyproject.toml` (`pygame==2.6.1`).

## Training

Train an agent headlessly (no window). Each algorithm writes to its own file by default, so runs don't overwrite each other:

```bash
./scripts/train.sh --algo ppo --timesteps 200000   # saves models/ppo_asteroids.zip
./scripts/train.sh --algo dqn --timesteps 200000   # saves models/dqn_asteroids.zip
```

Other options: `--n-envs` (parallel game copies), `--seed`, `--out` (custom output path), and `--checkpoint-every` (how often to save intermediate checkpoints). Trained models go in `models/`, which is gitignored.

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

The same controls are also shown in-game from the main menu's "Controls" screen.

## Game Notes

- On launch you get a main menu: Start Game, Controls, and Quit (navigate with Up/Down, select with Enter).
- The game runs at about 60 FPS.
- Asteroids spawn from screen edges.
- Large asteroids split into smaller, faster asteroids when shot.
- You gain points for staying alive and for each asteroid you destroy.
- You lose on collision with any asteroid; your score is then checked against the top-5 leaderboard.

## Logging Output

During a run, the game writes files in the project root (i.e. wherever `./scripts/play.sh` is invoked from):

- `game_state.jsonl`: periodic state snapshots
- `game_events.jsonl`: gameplay events (for example, asteroid split or player hit)
- `leaderboard.json`: persisted top-5 high scores (not overwritten between runs)

The two `.jsonl` logs are overwritten at the start of each new run.

## Project Structure

The installable package lives under `asteriod_game/` at the repo root.

- `main.py`: menu/controls state wiring, game loop, and sprite group wiring
- `constants.py`: global constants shared across the package (screen size, leaderboard file)
- `logger.py`: JSONL state/event logging
- `leaderboard.py`: top-5 high score persistence (`leaderboard.json`)
- `game/`: the actual gameplay
  - `circleshape.py`: base class for circle-collision sprites
  - `player.py`: ship movement, rotation, and shooting
  - `asteroid.py`: asteroid rendering, movement, and split behavior
  - `asteroidfield.py`: asteroid spawning logic
  - `shot.py`: bullet behavior
  - `score.py`: in-game score tracking and HUD
  - `constants.py`: gameplay-tunable values local to `game/`
- `ui/`: the screens shown before/around gameplay
  - `menu.py`: main menu (Start Game / Controls / Quit) with the leaderboard panel
  - `controls_screen.py`: "How to Play" screen
  - `constants.py`: UI layout/font values local to `ui/`
