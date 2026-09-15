from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.ui.constants import (
    MENU_TITLE_FONT_SIZE,
    MENU_OPTION_FONT_SIZE,
    CONTROLS_TEXT_FONT_SIZE,
    CONTROLS_LINE_SPACING,
)
import pygame

class ControlsScreen:
    LINES = [
        "W: move forward",
        "S: move backward",
        "A: rotate left",
        "D: rotate right",
        "Space: shoot",
        "Q: quit game",
    ]

    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        self.text_font = pygame.font.Font(None, CONTROLS_TEXT_FONT_SIZE)
        self.hint_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

    def run(self, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        return "menu"

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill("black")

        title_surface = self.title_font.render("How to Play", True, "white")
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6))
        self.screen.blit(title_surface, title_rect)

        top = SCREEN_HEIGHT / 3
        for i, line in enumerate(self.LINES):
            line_surface = self.text_font.render(line, True, "white")
            line_rect = line_surface.get_rect(center=(SCREEN_WIDTH / 2, top + i * CONTROLS_LINE_SPACING))
            self.screen.blit(line_surface, line_rect)

        hint_surface = self.hint_font.render("Press Enter to return to Main Menu", True, "yellow")
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))
        self.screen.blit(hint_surface, hint_rect)
