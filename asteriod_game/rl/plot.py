import argparse
import csv
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def read_games(run_dir):
    games = []
    for path in sorted(glob.glob(os.path.join(run_dir, "monitor_*.monitor.csv"))):
        with open(path) as f:
            lines = [line for line in f if not line.startswith("#")]
        for row in csv.DictReader(lines):
            games.append({
                "t": float(row["t"]),
                "reward": float(row["r"]),
                "length": int(row["l"]),
                "hits": int(row["hits"]),
                "died": int(row["died"]),
            })
    games.sort(key=lambda g: g["t"])
    return games

def read_updates(run_dir):
    path = os.path.join(run_dir, "progress.csv")
    if not os.path.exists(path):
        return [], []
    steps, losses = [], []
    with open(path) as f:
        for row in csv.DictReader(f):
            if row.get("train/loss") and row.get("time/total_timesteps"):
                steps.append(float(row["time/total_timesteps"]))
                losses.append(float(row["train/loss"]))
    return steps, losses

def rolling_mean(values, window):
    means = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1):i + 1]
        means.append(sum(chunk) / len(chunk))
    return means

def plot_run(run_dir, out_path=None):
    games = read_games(run_dir)
    if not games:
        raise SystemExit("No finished games found in " + run_dir + " (no monitor_*.monitor.csv rows)")
    episodes = list(range(1, len(games) + 1))
    window = max(1, len(games) // 20)
    update_steps, losses = read_updates(run_dir)

    panels = 4 if losses else 3
    fig, axes = plt.subplots(panels, 1, figsize=(9, 3 * panels), sharex=False)

    rewards = [g["reward"] for g in games]
    axes[0].plot(episodes, rewards, alpha=0.3, label="per game")
    axes[0].plot(episodes, rolling_mean(rewards, window), label="rolling mean")
    axes[0].set_ylabel("reward per game")
    axes[0].legend()

    lengths = [g["length"] for g in games]
    axes[1].plot(episodes, lengths, alpha=0.3)
    axes[1].plot(episodes, rolling_mean(lengths, window))
    axes[1].set_ylabel("length (frames)")

    hits = [g["hits"] for g in games]
    axes[2].plot(episodes, hits, alpha=0.3)
    axes[2].plot(episodes, rolling_mean(hits, window))
    axes[2].set_ylabel("asteroid hits")
    axes[2].set_xlabel("game number (across all copies, by finish time)")

    if losses:
        axes[3].plot(update_steps, losses)
        axes[3].set_ylabel("training loss")
        axes[3].set_xlabel("timesteps")

    fig.suptitle(os.path.basename(os.path.normpath(run_dir)))
    fig.tight_layout()
    out_path = out_path or os.path.join(run_dir, "plot.png")
    fig.savefig(out_path, dpi=100)
    plt.close(fig)
    return out_path

def main():
    parser = argparse.ArgumentParser(description="Plot training results for one run folder")
    parser.add_argument("run_dir")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    print("Saved plot to " + plot_run(args.run_dir, args.out))

if __name__ == "__main__":
    main()
