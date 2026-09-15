from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MENU_TITLE_FONT_SIZE,
    MENU_OPTION_FONT_SIZE,
    MENU_OPTION_SPACING,
    LEADERBOARD_PANEL_MARGIN,
    LEADERBOARD_HEADER_FONT_SIZE,
    LEADERBOARD_ENTRY_FONT_SIZE,
    LEADERBOARD_ENTRY_SPACING,
)
import pygame

class Menu:
    OPTIONS = [
        ("Start Game", "start"),
        ("Controls", "controls"),
        ("Quit", "quit"),
    ]

    def __init__(self, screen, leaderboard):
        self.screen = screen
        self.leaderboard = leaderboard
        self.selected_index = 0
        self.title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        self.option_font = pygame.font.Font(None, MENU_OPTION_FONT_SIZE)
        self.leaderboard_header_font = pygame.font.Font(None, LEADERBOARD_HEADER_FONT_SIZE)
        self.leaderboard_entry_font = pygame.font.Font(None, LEADERBOARD_ENTRY_FONT_SIZE)

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

        self.draw_leaderboard()

    def draw_leaderboard(self):
        x = SCREEN_WIDTH - LEADERBOARD_PANEL_MARGIN
        y = LEADERBOARD_PANEL_MARGIN

        header_surface = self.leaderboard_header_font.render("Leaderboard", True, "white")
        header_rect = header_surface.get_rect(topright=(x, y))
        self.screen.blit(header_surface, header_rect)

        y += header_rect.height + LEADERBOARD_ENTRY_SPACING / 2

        if not self.leaderboard.scores:
            empty_surface = self.leaderboard_entry_font.render("No scores yet", True, "white")
            empty_rect = empty_surface.get_rect(topright=(x, y))
            self.screen.blit(empty_surface, empty_rect)
            return

        for i, score in enumerate(self.leaderboard.scores):
            entry_surface = self.leaderboard_entry_font.render(f"{i + 1}. {score}", True, "white")
            entry_rect = entry_surface.get_rect(topright=(x, y + i * LEADERBOARD_ENTRY_SPACING))
            self.screen.blit(entry_surface, entry_rect)
