# Reading the Training Plots

Each `plot.png` (made by `./scripts/plot.sh`) shows how one training run went, compared with a random-play baseline. The horizontal axis counts finished games, so reading left to right shows progress over training.

## The lines

- **Faint blue line:** every single game. It's noisy, since some games go well by luck and some don't.
- **Orange line:** the rolling average over recent games. This is the line to read.
- **Dashed gray line:** the random baseline's average. Anything above it is better than random play.

## The four charts

1. **Reward per game (top):** points earned in each game. Higher is better. A rise followed by a flat orange line means the agent stopped improving.
2. **Length (frames):** how long each game lasted. At 60 frames per second, 1,000 frames is about 16 seconds. Longer means the ship survived longer.
3. **Asteroid hits:** asteroids shot in each game. Higher means more shooting. If the orange line sits on the dashed line, shooting hasn't improved.
4. **Training loss (bottom):** the learning signal, plotted against timesteps instead of games. It should trend down. Big early spikes are normal, and it settles into a low, bumpy line.

## Quick way to read it

Look at the orange line in each top chart and ask two questions:
- Is it above the dashed baseline line?
- Is it still going up at the right-hand end, or has it flattened?

## Single spikes

One very good or very bad game can produce a sharp spike in the faint blue line. The orange rolling average smooths these out, so a single spike only causes a short bump. Don't judge a run by one spike. Check whether similar games keep happening.

## Example: the first PPO run (1M timesteps, 8 copies)

- **Reward:** rose quickly over the first ~50 games, then levelled off at about 200. The random baseline is about 140, so the agent is clearly better than random.
- **Length:** about 1,000 frames throughout, rising slightly to about 1,100 after game ~300. The baseline is about 900. The ship survives somewhat longer.
- **Asteroid hits:** about 10 to 13 per game, against a baseline of about 10. Shooting barely improved.
- **Training loss:** large spikes early, then settling around 10.
- **Game ~200:** a single game with about 1,900 reward, 7,000 frames, and 85 hits. It's an outlier, and the rolling average only bumps briefly because of it.

**Reading:** the agent learned to survive, but not to hunt. Most of the reward comes from staying alive, since the score gives 10 points per second and each hit gives only 10 points.

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

## Logging Output

During a run, the game writes files into `results/`:

- `results/game_state.jsonl`: periodic state snapshots
- `results/game_events.jsonl`: gameplay events (for example, asteroid split or player hit)
- `results/leaderboard.json`: persisted top-5 high scores (not overwritten between runs)

The two `.jsonl` logs are overwritten at the start of each new run.
