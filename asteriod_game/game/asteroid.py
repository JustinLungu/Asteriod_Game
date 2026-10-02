from asteriod_game.game.circleshape import CircleShape
from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.game.constants import (
    LINE_WIDTH,
    ASTEROID_MIN_RADIUS,
    SPLIT_SPEED_INCREASE,
    ASTEROID_DESPAWN_MARGIN
)
from asteriod_game.logger import log_event
import pygame, random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

        if self.is_far_off_screen():
            self.kill()

    def is_far_off_screen(self):
        return (
            self.position.x < -ASTEROID_DESPAWN_MARGIN
            or self.position.x > SCREEN_WIDTH + ASTEROID_DESPAWN_MARGIN
            or self.position.y < -ASTEROID_DESPAWN_MARGIN
            or self.position.y > SCREEN_HEIGHT + ASTEROID_DESPAWN_MARGIN
        )

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        vel_ast_1 = self.velocity.rotate(angle)
        vel_ast_2 = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        ast_1 = Asteroid(self.position.x, self.position.y, new_radius)
        ast_2 = Asteroid(self.position.x, self.position.y, new_radius)
        ast_1.velocity = vel_ast_1 * SPLIT_SPEED_INCREASE
        ast_2.velocity = vel_ast_2 * SPLIT_SPEED_INCREASE