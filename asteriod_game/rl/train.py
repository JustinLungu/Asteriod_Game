from asteriod_game.rl.vec import make_vec_env
from stable_baselines3 import PPO
import argparse
import os

def train(timesteps, n_envs, seed, out):
    vec_env = make_vec_env(n_envs, seed=seed)
    try:
        model = PPO("MlpPolicy", vec_env, seed=seed, verbose=1)
        model.learn(total_timesteps=timesteps)
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        model.save(out)
    finally:
        vec_env.close()
    return out

def main():
    parser = argparse.ArgumentParser(description="Headless PPO training for Asteroids")
    parser.add_argument("--timesteps", type=int, default=100_000)
    parser.add_argument("--n-envs", type=int, default=4)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default="models/ppo_asteroids")
    args = parser.parse_args()
    path = train(args.timesteps, args.n_envs, args.seed, args.out)
    print("Saved model to " + path + ".zip")

if __name__ == "__main__":
    main()
