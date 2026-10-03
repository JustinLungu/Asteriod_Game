# Training Parameters

What each parameter does, its current value, and how it tends to affect performance.
Default values are taken from the installed stable-baselines3 version (2.9.0).

## Our command-line options (`scripts/train.sh`)

| Option | Default | What it does | Effect on performance |
|---|---|---|---|
| `--algo` | `ppo` | Algorithm: `ppo` or `dqn` | Changes the whole learning method and the action space. See the README for the tradeoffs. |
| `--timesteps` | `100000` | Total frames played across all game copies | The main lever for how much the agent can learn. Too few and it hasn't learned yet. |
| `--n-envs` | `4` | Number of game copies running in parallel | More copies collect data faster, and each update sees more varied games. Fewer updates happen for the same timesteps. Limited by free CPU cores. |
| `--seed` | `0` | Seeds the training run | Makes a run repeatable. It doesn't stop the asteroids from varying within a run. |
| `--checkpoint-every` | `50000` | Saves an intermediate model every this many timesteps | No effect on learning. Lets you compare early, middle, and late agents. |
| `--run-dir` | timestamped folder | Output folder to use | No effect on learning. |

## Our game settings (`asteriod_game/rl/constants.py` and `asteriod_game/rl/env.py`)

| Setting | Value | What it does | Effect on performance |
|---|---|---|---|
| `FIXED_DT` | `1/60` | Time step per frame used by training | Keeps game physics consistent during training. Changing it changes how fast the ship and asteroids move per step. |
| `DEATH_PENALTY` | `-100` | Reward subtracted when the ship dies | The main signal that dying is bad. Larger means avoiding death matters more. Too large can make the agent overly cautious. |
| `N_NEAREST_ASTEROIDS` | `10` | How many nearby asteroids the agent sees | More gives more information but slower learning. Fewer risks missing threats. |
| `REL_VELOCITY_SCALE` | `1/100` | Scales asteroid speed in the observation | Keeps input numbers in a range the network learns well. A poor choice can slow learning. |
| `SCORE_PER_ASTEROID_HIT` | `10` (in `game/constants.py`) | Points for each hit | Part of the reward. A hit is worth far less than surviving a few seconds. |
| `SCORE_PER_SECOND` | `10` (in `game/constants.py`) | Points per second alive | The main part of the reward, so the agent is largely rewarded for surviving. |
| `EPISODE_TIME_LIMIT_SECONDS` | `300` (in `game/constants.py`) | Maximum game length before it ends | Caps game length so training episodes don't run forever. |

## PPO parameters (what we use and what SB3 defaults to)

| Parameter | Our value | Default | What it does | Effect on performance |
|---|---|---|---|---|
| `learning_rate` | default | `0.0003` | Size of each adjustment to the network | Too high makes training unstable. Too low makes it slow. |
| `n_steps` | default | `2048` | Frames collected per game copy before each update | Longer rollouts give more context per update but fewer updates. |
| `batch_size` | default | `64` | Frames per gradient step | Smaller batches are noisier, larger ones steadier but slower per step. |
| `n_epochs` | default | `10` | Passes over each rollout | More passes learn more from each rollout, but can overfit to it and change the policy too much. |
| `gamma` | default | `0.99` | How much future rewards count compared with immediate ones | **Important here.** At 60 frames per second, 0.99 only looks about 1.7 seconds ahead. Dangers further away barely count. A value like `0.999` looks about 16 seconds ahead. |
| `gae_lambda` | default | `0.95` | Balances short and long estimates of how good an action was | Lower trusts short-term estimates more, higher trusts long-term ones more. Rarely needs changing. |
| `clip_range` | default | `0.2` | Caps how far the policy can change in one update | Keeps updates from being too large. Too small slows learning. |
| `ent_coef` | default | `0.0` | Bonus for keeping the policy random | Higher keeps the agent exploring for longer. At 0, the agent can settle into one habit early. |
| `vf_coef` | default | `0.5` | Weight of the value-prediction error in the total loss | Balances how much learning goes into predicting reward versus choosing actions. |
| `max_grad_norm` | default | `0.5` | Caps the size of a gradient step | Prevents one unusual batch from causing a large, damaging update. |

## DQN parameters (what we use and what SB3 defaults to)

| Parameter | Our value | Default | What it does | Effect on performance |
|---|---|---|---|---|
| `learning_rate` | default | `0.0001` | Size of each adjustment to the network | Same tradeoff as PPO. |
| `buffer_size` | default | `1000000` | How many past frames DQN remembers and learns from | Larger keeps more varied experience. Smaller forgets older experience faster. |
| `learning_starts` | default | `100` | Frames collected before learning begins | Small, so learning starts almost immediately. |
| `batch_size` | default | `32` | Frames sampled from memory per gradient step | Same tradeoff as PPO's batch size. |
| `gamma` | default | `0.99` | Same as PPO's `gamma` | Same caveat: a short look-ahead. |
| `train_freq` | default | `4` | Frames played between learning steps | Less frequent learning is faster per frame but adapts more slowly. |
| `target_update_interval` | default | `10000` | Frames between refreshes of DQN's stable reference network | Too frequent can destabilize learning. Too rare slows it. |
| `exploration_fraction` | default | `0.1` | Share of training during which random actions decrease | At 1M timesteps, exploration falls over the first 100k. After that the agent mostly plays its best guess. |
| `exploration_initial_eps` | default | `1.0` | Starting share of random actions | Starts fully random. |
| `exploration_final_eps` | default | `0.05` | Share of random actions after the decrease | 5% random presses even late in training, which can keep some noise in play. |

## Logging and saving (not learning settings)

| Component | What it does |
|---|---|
| `Monitor` (per game copy) | Writes one row per finished game to `monitor_<n>.monitor.csv`. Records reward, length, time, score, hits, splits, died, timed out. Doesn't affect learning. |
| `CheckpointCallback` | Saves models every `--checkpoint-every` steps. Doesn't affect learning. |
| SB3 logger (`progress.csv`) | Writes training statistics every update. Doesn't affect learning. |
