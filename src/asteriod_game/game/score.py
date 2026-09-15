from asteriod_game.game.constants import (
    SCORE_PER_SECOND,
    SCORE_FONT_SIZE,
    SCORE_MARGIN,
)
import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.points = 0
        self.timer = 0.0
        self.font = pygame.font.Font(None, SCORE_FONT_SIZE)

    def update(self, dt):
        self.timer += dt
        while self.timer >= 1.0:
            self.timer -= 1.0
            self.points += SCORE_PER_SECOND

    def add_points(self, points):
        self.points += points

    def draw(self, screen):
        text = self.font.render(f"Score: {self.points}", True, "white")
        screen.blit(text, (SCORE_MARGIN, SCORE_MARGIN))
