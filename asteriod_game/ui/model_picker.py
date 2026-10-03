from asteriod_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteriod_game.ui.constants import (
    MENU_TITLE_FONT_SIZE,
    PICKER_FONT_SIZE,
    PICKER_ROW_SPACING,
    PICKER_VISIBLE_ROWS,
    KEY_REPEAT_DELAY_MS,
    KEY_REPEAT_INTERVAL_MS,
)
import pygame

class ModelPicker:
    def __init__(self, screen, title, entries):
        self.screen = screen
        self.title = title
        self.entries = entries
        self.selected_index = 0
        self.title_font = pygame.font.Font(None, MENU_TITLE_FONT_SIZE)
        self.row_font = pygame.font.Font(None, PICKER_FONT_SIZE)

    def run(self, clock):
        pygame.key.set_repeat(KEY_REPEAT_DELAY_MS, KEY_REPEAT_INTERVAL_MS)
        try:
            return self._loop(clock)
        finally:
            pygame.key.set_repeat()

    def _loop(self, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if not self.entries:
                        continue
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.entries)
                    if event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.entries)
                    if event.key == pygame.K_RETURN:
                        return self.entries[self.selected_index][1]

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill("black")
        title = self.title_font.render(self.title, True, "white")
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH / 2, 60)))

        if not self.entries:
            message = self.row_font.render("Nothing here yet. Train a model first. Press Esc to go back.", True, "yellow")
            self.screen.blit(message, message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
            return

        start = max(0, min(self.selected_index - PICKER_VISIBLE_ROWS // 2, len(self.entries) - PICKER_VISIBLE_ROWS))
        visible = self.entries[start:start + PICKER_VISIBLE_ROWS]
        top = 130
        for row, (label, _path) in enumerate(visible):
            index = start + row
            color = "yellow" if index == self.selected_index else "white"
            surface = self.row_font.render(label, True, color)
            self.screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH / 2, top + row * PICKER_ROW_SPACING)))

        hint = self.row_font.render("Up/Down to choose, Enter to watch, Esc to go back", True, "white")
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40)))
