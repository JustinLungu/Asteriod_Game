from asteriod_game.rl.env import GameEnv
from asteriod_game.rl.wrappers import DiscreteActionWrapper
from asteriod_game.rl.algorithms import ALGORITHMS
import json
import os
import pygame

class LoadedPolicy:
    def __init__(self, model_path):
        run_dir = os.path.dirname(model_path)
        metadata_path = os.path.join(run_dir, "metadata.json")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError("No metadata.json next to " + model_path + "; cannot tell which algorithm to load")
        with open(metadata_path) as f:
            self.algo = json.load(f)["algo"]
        self.uses_dqn_actions = ALGORITHMS[self.algo][1]
        self.model = ALGORITHMS[self.algo][0].load(model_path)

    def make_env(self):
        pygame.font.init()
        env = GameEnv()
        if self.uses_dqn_actions:
            env = DiscreteActionWrapper(env)
        return env

    def act(self, observation):
        action, _ = self.model.predict(observation, deterministic=True)
        return action
