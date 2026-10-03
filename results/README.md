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
