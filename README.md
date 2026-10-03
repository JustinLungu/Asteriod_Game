# Asteroid Game

A small arcade-style Asteroids clone built with Python and `pygame`, plus a reinforcement learning
agent (PPO and DQN via stable-baselines3) that learns to play it.

You control a ship, dodge incoming asteroids, and blast them into smaller pieces.

## Requirements

- Python `3.13+`
- [`uv`](https://docs.astral.sh/uv/) for environment and dependency management

## Quick Start

```bash
uv sync
./scripts/play.sh
```

The main menu has four options: **Start Game**, **Controls**, **Watch AI**, and **Quit**. Navigate with Up/Down and select with Enter (holding Up or Down keeps scrolling).

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

The same controls are also shown in-game from the main menu's "Controls" screen. Press Enter or Esc there to go back to the menu.

## Game Notes

- When a game ends (you're hit or the time limit runs out), you return to the main menu, where you can start another game. After a watched game, you return to the stage list instead, to compare stages.
- The game runs at about 60 FPS.
- Asteroids spawn from screen edges.
- Large asteroids split into smaller, faster asteroids when shot.
- You gain points for staying alive and for each asteroid you destroy.
- You lose on collision with any asteroid; your score is then checked against the top-5 leaderboard.

## AI: Train and Watch

Train an agent, then watch what it learned:

```bash
./scripts/train.sh --algo ppo --timesteps 1000000
./scripts/baseline.sh --episodes 100
./scripts/plot.sh results/models/<time>_ppo --baseline results/baselines/<time>_random
```

Watch a model from the menu with **Watch AI**, or from the command line with `./scripts/watch.sh --model <path>`.

- Full training and watching guide: [`asteriod_game/rl/README.md`](asteriod_game/rl/README.md)
- Reading the stats, plots, and output files: [`results/README.md`](results/README.md)

## Project Structure

The installable package lives under `asteriod_game/` at the repo root.

- `main.py`: menu/controls state wiring, game loop, and sprite group wiring
- `constants.py`: global constants shared across the package (screen size, leaderboard file)
- `logger.py`: JSONL state/event logging
- `leaderboard.py`: top-5 high score persistence (`results/leaderboard.json`)
- `rl/`: the AI side: the Gymnasium environment, training, playback, plots, and their docs (see `rl/README.md`)
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
- `scripts/`: one-line commands for playing, training, baselines, plots, and watching
