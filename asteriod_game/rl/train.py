from asteriod_game.rl.vec import make_vec_env
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.callbacks import CheckpointCallback
import argparse
import os

ALGORITHMS = {
    "ppo": (PPO, False),
    "dqn": (DQN, True),
}

def train(timesteps, n_envs, seed, out, checkpoint_every, algo):
    algorithm, use_dqn_actions = ALGORITHMS[algo]
    vec_env = make_vec_env(n_envs, seed=seed, use_dqn_actions=use_dqn_actions)
    checkpoint_dir = os.path.dirname(out) or "."
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoints = CheckpointCallback(
        save_freq=max(1, checkpoint_every // n_envs),
        save_path=checkpoint_dir,
        name_prefix=os.path.basename(out) + "_checkpoint",
    )
    try:
        model = algorithm("MlpPolicy", vec_env, seed=seed, verbose=1)
        model.learn(total_timesteps=timesteps, callback=checkpoints)
        model.save(out)
    finally:
        vec_env.close()
    return out

def main():
    parser = argparse.ArgumentParser(description="Headless training for Asteroids")
    parser.add_argument("--algo", choices=sorted(ALGORITHMS), default="ppo")
    parser.add_argument("--timesteps", type=int, default=100_000)
    parser.add_argument("--n-envs", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default="models/ppo_asteroids")
    parser.add_argument("--checkpoint-every", type=int, default=50_000)
    args = parser.parse_args()
    path = train(args.timesteps, args.n_envs, args.seed, args.out, args.checkpoint_every, args.algo)
    print("Saved model to " + path + ".zip")

if __name__ == "__main__":
    main()
