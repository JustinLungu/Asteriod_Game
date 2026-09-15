from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MENU_TITLE_FONT_SIZE,
    MENU_OPTION_FONT_SIZE,
    MENU_OPTION_SPACING,
)
import pygame

class Menu:
    OPTIONS = [
        ("Start Game", "start"),
        ("Controls", "controls"),
        ("Quit", "quit"),
    ]

    def __init__(self, screen):
        self.screen = screen
        self.selected_index = 0
        self.title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        self.option_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)

    def run(self, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.OPTIONS)
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.OPTIONS)
                    if event.key == pygame.K_RETURN:
                        return self.OPTIONS[self.selected_index][1]

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill("black")

        title_surface = self.title_font.render("Welcome to Asteroid Game", True, "white")
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        self.screen.blit(title_surface, title_rect)

        for i, (label, _action) in enumerate(self.OPTIONS):
            color = "yellow" if i == self.selected_index else "white"
            option_surface = self.option_font.render(label, True, color)
            option_rect = option_surface.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * MENU_OPTION_SPACING)
            )
            self.screen.blit(option_surface, option_rect)
