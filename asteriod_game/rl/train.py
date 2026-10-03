from asteriod_game.rl.vec import make_vec_env
from asteriod_game.rl.algorithms import ALGORITHMS
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure
from datetime import datetime
import argparse
import json
import os
import stable_baselines3

MODELS_DIR = "results/models"

def make_run_dir(algo, now):
    return os.path.join(MODELS_DIR, now.strftime("%Y-%m-%d_%H-%M-%S") + "_" + algo)

def train(timesteps, n_envs, seed, run_dir, checkpoint_every, algo):
    algorithm, use_dqn_actions = ALGORITHMS[algo]
    os.makedirs(run_dir, exist_ok=True)
    started = datetime.now()

    vec_env = make_vec_env(n_envs, seed=seed, use_dqn_actions=use_dqn_actions, log_dir=run_dir)
    checkpoints = CheckpointCallback(
        save_freq=max(1, checkpoint_every // n_envs),
        save_path=run_dir,
        name_prefix="checkpoint",
    )
    try:
        model = algorithm("MlpPolicy", vec_env, seed=seed, verbose=1)
        model.set_logger(configure(run_dir, ["stdout", "csv"]))
        model.learn(total_timesteps=timesteps, callback=checkpoints)
        final_path = os.path.join(run_dir, "final")
        model.save(final_path)
        trained_timesteps = model.num_timesteps
    finally:
        vec_env.close()

    finished = datetime.now()
    metadata = {
        "algo": algo,
        "timesteps_requested": timesteps,
        "timesteps_trained": trained_timesteps,
        "n_envs": n_envs,
        "seed": seed,
        "checkpoint_every": checkpoint_every,
        "started": started.isoformat(timespec="seconds"),
        "finished": finished.isoformat(timespec="seconds"),
        "duration_seconds": round((finished - started).total_seconds(), 1),
        "stable_baselines3_version": stable_baselines3.__version__,
    }
    with open(os.path.join(run_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    return final_path

def main():
    parser = argparse.ArgumentParser(description="Headless training for Asteroids")
    parser.add_argument("--algo", choices=sorted(ALGORITHMS), default="ppo")
    parser.add_argument("--timesteps", type=int, default=100_000)
    parser.add_argument("--n-envs", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--run-dir", default=None)
    parser.add_argument("--checkpoint-every", type=int, default=50_000)
    args = parser.parse_args()
    run_dir = args.run_dir or make_run_dir(args.algo, datetime.now())
    path = train(args.timesteps, args.n_envs, args.seed, run_dir, args.checkpoint_every, args.algo)
    print("Saved model to " + path + ".zip")
    print("Run folder: " + run_dir)

if __name__ == "__main__":
    main()
