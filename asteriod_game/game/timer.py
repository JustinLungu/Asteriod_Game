from asteriod_game.constants import SCREEN_WIDTH
from asteriod_game.game.constants import (
    EPISODE_TIME_LIMIT_SECONDS,
    TIMER_FONT_SIZE,
    TIMER_MARGIN,
)
import pygame

class Timer(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.remaining = EPISODE_TIME_LIMIT_SECONDS
        self.font = pygame.font.Font(None, TIMER_FONT_SIZE)

    def update(self, dt):
        self.remaining = max(0.0, self.remaining - dt)

    def is_expired(self):
        return self.remaining <= 0

    def draw(self, screen):
        minutes, seconds = divmod(int(self.remaining), 60)
        text = self.font.render(f"Time: {minutes:02d}:{seconds:02d}", True, "white")
        text_rect = text.get_rect(topright=(SCREEN_WIDTH - TIMER_MARGIN, TIMER_MARGIN))
        screen.blit(text, text_rect)
