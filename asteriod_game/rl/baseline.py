from asteriod_game.rl.env import GameEnv
from asteriod_game.rl.vec import MONITOR_KEYWORDS
from datetime import datetime
from stable_baselines3.common.monitor import Monitor
import argparse
import json
import os
import pygame

BASELINES_DIR = "results/baselines"

def make_baseline_dir(now):
    return os.path.join(BASELINES_DIR, now.strftime("%Y-%m-%d_%H-%M-%S") + "_random")

def run_baseline(episodes, seed, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    started = datetime.now()

    pygame.font.init()
    env = Monitor(GameEnv(), filename=os.path.join(out_dir, "monitor_0"), info_keywords=MONITOR_KEYWORDS)
    env.action_space.seed(seed)
    env.reset(seed=seed)
    try:
        for _ in range(episodes):
            env.reset()
            done = False
            while not done:
                _, _, terminated, truncated, _ = env.step(env.action_space.sample())
                done = terminated or truncated
    finally:
        env.close()

    finished = datetime.now()
    metadata = {
        "policy": "uniform random actions",
        "episodes": episodes,
        "seed": seed,
        "started": started.isoformat(timespec="seconds"),
        "finished": finished.isoformat(timespec="seconds"),
        "duration_seconds": round((finished - started).total_seconds(), 1),
    }
    with open(os.path.join(out_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    return out_dir

def main():
    parser = argparse.ArgumentParser(description="Random-action baseline for comparison plots")
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--run-dir", default=None)
    args = parser.parse_args()
    out_dir = args.run_dir or make_baseline_dir(datetime.now())
    print("Saved baseline to " + run_baseline(args.episodes, args.seed, out_dir))

if __name__ == "__main__":
    main()
