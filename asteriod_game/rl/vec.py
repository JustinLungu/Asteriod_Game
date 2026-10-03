from asteriod_game.rl.env import GameEnv
from asteriod_game.rl.wrappers import DiscreteActionWrapper
from stable_baselines3.common.vec_env import SubprocVecEnv
import pygame

def _make_env(use_dqn_actions):
    def _init():
        pygame.font.init()
        env = GameEnv()
        if use_dqn_actions:
            env = DiscreteActionWrapper(env)
        return env
    return _init

def make_vec_env(n_envs, seed=None, use_dqn_actions=False):
    env_fns = []
    for _ in range(n_envs):
        env_fns.append(_make_env(use_dqn_actions))
    vec_env = SubprocVecEnv(env_fns)
    if seed is not None:
        vec_env.seed(seed)
    return vec_env
