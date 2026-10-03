from asteriod_game.rl.env import GameEnv
from asteriod_game.rl.wrappers import DiscreteActionWrapper
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv
import os
import pygame

MONITOR_KEYWORDS = ("score", "hits", "splits", "died", "timed_out", "boundary_frames")

def _make_env(use_dqn_actions, monitor_path):
    def _init():
        pygame.font.init()
        env = GameEnv()
        if use_dqn_actions:
            env = DiscreteActionWrapper(env)
        if monitor_path is not None:
            env = Monitor(env, filename=monitor_path, info_keywords=MONITOR_KEYWORDS)
        return env
    return _init

def make_vec_env(n_envs, seed=None, use_dqn_actions=False, log_dir=None):
    env_fns = []
    for i in range(n_envs):
        monitor_path = None
        if log_dir is not None:
            monitor_path = os.path.join(log_dir, "monitor_" + str(i))
        env_fns.append(_make_env(use_dqn_actions, monitor_path))
    vec_env = SubprocVecEnv(env_fns)
    if seed is not None:
        vec_env.seed(seed)
    return vec_env
