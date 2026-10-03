from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.game.constants import (
    SCORE_PER_ASTEROID_HIT,
    ASTEROID_MAX_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
)
from asteriod_game.game.actions import Actions
from asteriod_game.game.player import Player
from asteriod_game.game.asteroid import Asteroid
from asteriod_game.game.asteroidfield import AsteroidField
from asteriod_game.game.shot import Shot
from asteriod_game.game.score import Score
from asteriod_game.game.timer import Timer
from asteriod_game.rl.constants import (
    FIXED_DT,
    N_NEAREST_ASTEROIDS,
    PLAYER_OBSERVATION_SIZE,
    ASTEROID_OBSERVATION_SIZE,
    OBSERVATION_SIZE,
    REL_VELOCITY_SCALE,
    DEATH_PENALTY,
)
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random

class GameEnv(gym.Env):
    def __init__(self):
        super().__init__()
        # 5 independent booleans, matching Actions: rotate_left, rotate_right,
        # thrust_forward, thrust_backward, shoot
        self.action_space = spaces.MultiBinary(5)

        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(OBSERVATION_SIZE,), dtype=np.float32)

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
        if seed is not None:
            random.seed(seed)

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
        score_before = self.score.points

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
                    if asteroid.split():
                        events.append("asteroid_split")
                    shot.kill()
                    self.score.add_points(SCORE_PER_ASTEROID_HIT)

        truncated = self.timer.is_expired()

        reward = self.score.points - score_before
        if terminated:
            reward += DEATH_PENALTY

        observation = self._get_observation()
        info = {"score": self.score.points, "events": events}

        return observation, reward, terminated, truncated, info

    def _get_observation(self):
        obs = np.zeros(OBSERVATION_SIZE, dtype=np.float32)

        forward = pygame.Vector2(0, 1).rotate(self.player.rotation)
        cooldown = min(max(self.player.cooldown_timer, 0.0) / PLAYER_SHOOT_COOLDOWN_SECONDS, 1.0)
        obs[0] = self.player.position.x / SCREEN_WIDTH * 2 - 1
        obs[1] = self.player.position.y / SCREEN_HEIGHT * 2 - 1
        obs[2] = forward.x
        obs[3] = forward.y
        obs[4] = cooldown

        nearest = sorted(
            self.asteroids,
            key=lambda asteroid: asteroid.position.distance_to(self.player.position),
        )[:N_NEAREST_ASTEROIDS]

        for i, asteroid in enumerate(nearest):
            start = PLAYER_OBSERVATION_SIZE + i * ASTEROID_OBSERVATION_SIZE
            rel_pos = asteroid.position - self.player.position
            rel_vel = asteroid.velocity - self.player.velocity
            obs[start] = 1.0
            obs[start + 1] = rel_pos.x / SCREEN_WIDTH
            obs[start + 2] = rel_pos.y / SCREEN_HEIGHT
            obs[start + 3] = rel_vel.x * REL_VELOCITY_SCALE
            obs[start + 4] = rel_vel.y * REL_VELOCITY_SCALE
            obs[start + 5] = asteroid.radius / ASTEROID_MAX_RADIUS

        return obs
