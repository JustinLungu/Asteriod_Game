from asteriod_game.game.circleshape import CircleShape
from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.game.constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS
)
from asteriod_game.game.shot import Shot
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        self.touched_boundary = False

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def update(self, dt, actions):
        self.cooldown_timer -= dt

        if actions.rotate_left:
            self.rotate(dt * -1)
        if actions.rotate_right:
            self.rotate(dt)
        if actions.thrust_forward:
            self.move(dt)
        if actions.thrust_backward:
            self.move(dt * -1)
        if actions.shoot:
            if self.cooldown_timer <= 0:
                self.shoot()
                self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        self.touched_boundary = self.clamp_to_screen()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        unit_vector *= PLAYER_SPEED * dt
        self.position += unit_vector

    def clamp_to_screen(self):
        before = pygame.Vector2(self.position)
        self.position.x = max(self.radius, min(self.position.x, SCREEN_WIDTH - self.radius))
        self.position.y = max(self.radius, min(self.position.y, SCREEN_HEIGHT - self.radius))
        return self.position != before

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED