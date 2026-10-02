from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.game.constants import SCORE_PER_ASTEROID_HIT
from asteriod_game.game.actions import Actions
from asteriod_game.game.player import Player
from asteriod_game.game.asteroid import Asteroid
from asteriod_game.game.asteroidfield import AsteroidField
from asteriod_game.game.shot import Shot
from asteriod_game.game.score import Score
from asteriod_game.game.timer import Timer
from asteriod_game.rl.constants import FIXED_DT
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class GameEnv(gym.Env):
    def __init__(self):
        super().__init__()
        # 5 independent booleans, matching Actions: rotate_left, rotate_right,
        # thrust_forward, thrust_backward, shoot
        self.action_space = spaces.MultiBinary(5)

        # placeholder; real observation design is feature/rl-observation-reward
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(1,), dtype=np.float32)

        self.updatable = None
        self.drawable = None
        self.asteroids = None
        self.shots = None
        self.player = None
        self.asteroid_field = None
        self.score = None
        self.timer = None

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        Player.containers = (self.drawable,)
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        self.asteroid_field = AsteroidField()

        Shot.containers = (self.shots, self.updatable, self.drawable)

        Score.containers = (self.updatable, self.drawable)
        self.score = Score()

        Timer.containers = (self.updatable, self.drawable)
        self.timer = Timer()

        return self._get_observation(), {}

    def step(self, action):
        actions = Actions.from_array(action)

        self.updatable.update(FIXED_DT)
        self.player.update(FIXED_DT, actions)

        events = []
        terminated = False
        for asteroid in self.asteroids:
            if asteroid.collides_with(self.player):
                terminated = True
                break

            for shot in self.shots:
                if asteroid.collides_with(shot):
                    events.append("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    self.score.add_points(SCORE_PER_ASTEROID_HIT)

        truncated = self.timer.is_expired()

        # placeholder; real reward design is feature/rl-observation-reward
        reward = 0.0

        observation = self._get_observation()
        info = {"score": self.score.points, "events": events}

        return observation, reward, terminated, truncated, info

    def _get_observation(self):
        # placeholder; real observation design is feature/rl-observation-reward
        return np.zeros(1, dtype=np.float32)
