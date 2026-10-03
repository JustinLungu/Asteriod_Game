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

Training runs headlessly (no window). Every run is saved in its own folder, so runs never overwrite each other.

### Workflow

1. **Train an agent**

   ```bash
   ./scripts/train.sh --algo ppo --timesteps 1000000
   ```

   This creates `results/models/<time>_ppo/`, which contains `final.zip` (the trained model), the checkpoints, `metadata.json`, `monitor_<n>.monitor.csv` (one row per finished game), and `progress.csv` (training statistics per update).

2. **Record a random baseline** (once is enough, unless you want a bigger sample)

   ```bash
   ./scripts/baseline.sh --episodes 100
   ```

   This creates `results/baselines/<time>_random/`, which plays uniformly random button presses. It gives you a reference to compare against.

3. **Plot the run against the baseline**

   ```bash
   ./scripts/plot.sh results/models/<time>_ppo --baseline results/baselines/<time>_random
   ```

   This writes `plot.png` into the run folder. The dashed line is the baseline's average.

To use the newest run without copying its name, run `ls -td results/models/*_ppo | head -1` (or `*_dqn`, or `results/baselines/*_random` for the baseline). Plugging that output into the commands above saves typing.

### Options

| Command | Option | Default | What it does |
|---|---|---|---|
| `train.sh` | `--algo` | `ppo` | `ppo` or `dqn` |
| `train.sh` | `--timesteps` | `100000` | total frames to play across all game copies |
| `train.sh` | `--n-envs` | `4` | number of game copies running in parallel |
| `train.sh` | `--seed` | `0` | makes a run repeatable |
| `train.sh` | `--checkpoint-every` | `50000` | how often to save intermediate checkpoints |
| `train.sh` | `--run-dir` | timestamped folder | use a specific output folder instead |
| `baseline.sh` | `--episodes` | `50` | number of random games to record |
| `baseline.sh` | `--seed` | `0` | makes the baseline repeatable |
| `baseline.sh` | `--run-dir` | timestamped folder | use a specific output folder instead |
| `plot.sh` | `--baseline` | none | folder of a baseline to draw as a reference line |
| `plot.sh` | `--out` | `plot.png` in the run folder | where to save the image |

**Comparing algorithms:** train with `--algo dqn` the same way. Plot each run separately, or plot a PPO run against the same baseline to compare the two.

**Using more game copies:** `--n-envs` makes collection faster, up to about the number of free CPU cores. See "How Training Works" below for the tradeoffs.

All outputs go in `results/`, which is gitignored.

## Watching a Trained Model

Watch a trained agent play one game in a window. It works with final models and with checkpoints from the middle of training, so you can compare an early, middle, and final agent.

```bash
./scripts/watch.sh --model results/models/<time>_ppo/final.zip
./scripts/watch.sh --model results/models/<time>_ppo/checkpoint_50000_steps.zip
./scripts/watch.sh --model results/models/<time>_dqn/final.zip
```

To see what checkpoints a run has, list its folder: `ls results/models/<time>_ppo/`. Checkpoint numbers are total timesteps, so a larger number is later in training.

By default each watch gets a different asteroid sequence, just as training does. To compare checkpoints fairly, pass the same `--seed` to each one so they face identical asteroids:

```bash
./scripts/watch.sh --model results/models/<time>_ppo/checkpoint_50000_steps.zip --seed 1
./scripts/watch.sh --model results/models/<time>_ppo/final.zip --seed 1
```

The window shows the algorithm and file name in the bottom-left corner. Press **Esc** to stop early. The game ends when the ship dies or the time limit is reached, and the final score is printed in the terminal. Watching doesn't change the leaderboard.

## How Training Works

Training alternates between two phases: the agent plays to collect experience, then it learns from that experience.

**Rollouts and updates (PPO)**
- Each update starts by playing 2,048 frames with the current agent. These frames are discarded after the update, because the agent changes every update and old frames describe an older version of it.
- During the update, the frames are cut into minibatches of 64 and the agent makes 10 passes (epochs) over them. That's 32 gradient steps per pass, or 320 per update.
- With `--timesteps 200000` and one game copy, that's about 98 updates, 980 epochs, and roughly 31,000 gradient steps.

**Episodes vs. rollouts**
- An episode is one full game, from start to death or the time limit.
- A rollout is a fixed 2,048 frames, regardless of game boundaries. One rollout can contain several short episodes, and one long episode can span several rollouts.

**What `--n-envs` does**
- Each game copy fills its own 2,048 frames at the same time. With 4 copies, one update learns from 8,192 frames.
- When a copy dies, it resets and keeps playing, so no copy sits idle.
- Collection is faster, and each minibatch mixes frames from different games, which makes learning steadier.
- Each update session sees more frames produced by the same weights, so the agent gets a broader picture of how its current policy behaves before it changes. This is the variety benefit, not extra exploration: exploration comes from PPO sampling its actions from probabilities, and `--timesteps` sets how much total experience there is.
- The tradeoff: with the same timesteps there are fewer updates (about 25 instead of 98), so the agent changes its behavior less often. The total gradient steps stay about the same, so learning itself isn't sped up. More copies also cost CPU cores and RAM, and past the number of free cores they stop helping.

**PPO vs. DQN**
- PPO works with five on/off switches, so it can press several actions at once.
- DQN chooses one entry from a list. The DQN wrapper turns its 32 choices into every combination of the five switches. PPO and human play use the original switches and are unaffected.
- Both use `MlpPolicy`, the same kind of neural network. The output differs: one probability per action for PPO, one score per combination for DQN.

**Hardware**
- The training uses the GPU automatically when PyTorch can see one. The network is small, so the game simulation on the CPU is usually the bottleneck, which is why `--n-envs` matters more than the GPU for speed.

## Reading the Training Stats

While training, SB3 prints a table every update. Here's what each row means.

**How the game is going (rollout)**
- **ep_rew_mean:** average reward per game over recent games. This is the main one to watch: it should trend upward over training.
- **ep_len_mean:** average game length in frames. At 60 frames per second, 950 frames is about 16 seconds of survival. Longer generally means the agent is surviving better.

**How fast it's running (time)**
- **fps:** frames per second across all game copies together.
- **iterations:** how many update sessions have finished. Each one collects a fresh rollout.
- **time_elapsed:** seconds since training started.
- **total_timesteps:** total frames played so far. With 8 copies and 2,048 frames each, one session adds 16,384 frames.

**What the learning step is doing (train)**
- **n_updates:** passes over the data (epochs) completed so far. 50 means 5 learning rounds of 10 epochs each.
- **approx_kl:** how much the policy changed in the last update. Small is good. If it climbs, the agent is changing too fast.
- **clip_fraction** and **clip_range:** PPO caps how far the policy can move in one update, by 20% (`clip_range` 0.2). The fraction is how often that cap was hit. About 6% is normal. Much higher means the learning rate may be too high.
- **entropy_loss:** the negative of the policy's entropy, which measures how random its button presses still are. The sign is flipped, so −3.42 means an entropy of 3.42. It should slowly drop as the agent becomes more decisive, but not to zero too early.
- **explained_variance:** how well the agent predicts the rewards it will actually get. 1 is perfect, 0 is no better than guessing the average, and negative is worse than guessing. Values near 0.2 are weak but normal early on, and should rise.
- **learning_rate:** how big each adjustment is. It's SB3's default and stays constant here.
- **loss**, **policy_gradient_loss**, **value_loss:** the total loss adds three parts. The policy part is close to zero when healthy. The value part usually dominates, because rewards are large: scores reach hundreds and the death penalty is −100. Value loss should fall as explained_variance rises.

**What to look for over a long run:** ep_rew_mean and explained_variance rising, value_loss falling, entropy slowly falling, and approx_kl and clip_fraction staying small. If the reward flattens while entropy keeps falling, the agent has settled into one way of playing.

### DQN stats

DQN prints a different table, because it learns differently from PPO.

- **exploration_rate:** how often DQN picks a random action instead of its best guess. It starts near 1.0 and falls over time. At 0.05, it's mostly playing its best guess now. PPO has no equivalent, since it explores by sampling its own probabilities.
- **episodes:** the number of finished games so far. PPO doesn't print this.
- **loss:** DQN's single learning signal. Its scale is different from PPO's loss, so don't compare the two numbers directly.
- **n_updates:** individual gradient steps taken so far. For PPO this counted epochs, so the same name means something different here.
- **fps:** usually much higher than PPO's. DQN takes a small learning step every few frames, instead of collecting a large rollout and making several passes over it. That makes each frame cheaper, not more useful, so compare algorithms by reward against `total_timesteps`, not against `time_elapsed`.

The DQN table has no `explained_variance`, `value_loss`, `approx_kl`, or `clip_fraction`, because those belong to PPO's learning step.

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

During a run, the game writes files into `results/`:

- `results/game_state.jsonl`: periodic state snapshots
- `results/game_events.jsonl`: gameplay events (for example, asteroid split or player hit)
- `results/leaderboard.json`: persisted top-5 high scores (not overwritten between runs)

The two `.jsonl` logs are overwritten at the start of each new run.

## Project Structure

The installable package lives under `asteriod_game/` at the repo root.

- `main.py`: menu/controls state wiring, game loop, and sprite group wiring
- `constants.py`: global constants shared across the package (screen size, leaderboard file)
- `logger.py`: JSONL state/event logging
- `leaderboard.py`: top-5 high score persistence (`results/leaderboard.json`)
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
