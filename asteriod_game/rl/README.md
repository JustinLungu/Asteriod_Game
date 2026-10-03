# Training and Watching the AI

This folder contains the reinforcement learning side of the game: the environment the agent plays,
the training scripts, and the tools for watching and comparing trained agents.

- Parameter reference (what every setting does and how it affects learning): [PARAMETERS.md](PARAMETERS.md)
- Reading the training stats, plots, and output files: [`results/README.md`](../../results/README.md)

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

For what each parameter does and how it affects performance, see `asteriod_game/rl/PARAMETERS.md`.

All outputs go in `results/`, which is gitignored.

## Watching a Trained Model

Watch a trained agent play one game in a window. It works with final models and with checkpoints from the middle of training, so you can compare an early, middle, and final agent.

### From the menu

1. Run `./scripts/play.sh`.
2. Choose **Watch AI** and press Enter.
3. **Choose a run.** The first list shows each training run, newest first, with its algorithm and how many timesteps it trained for. Choose one with Up/Down and press Enter.
4. **Choose a stage.** The second list shows that run's stages: `final`, then each checkpoint with its timestep count (`50,000 steps`, `100,000 steps`, and so on). Checkpoint numbers are total timesteps, so a larger number is later in training. Choose a stage and press Enter.
5. The agent plays one game in its own window, labelled with the run, the stage, and the algorithm. The menu window closes while it plays and reopens afterwards. Press **Esc** to stop early, or wait for the ship to die or the time limit to run out.
6. When the game ends, you return to the stage list of the same run. Pick another stage to compare, or press Esc to go back to the run list. Press Esc again to return to the main menu.

Closing the window at any point quits the program. If there are no runs yet, the list says so; train a model first (see "Training" above).

### From the command line

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
