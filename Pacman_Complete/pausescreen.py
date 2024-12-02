# FILE: pause_screen.py

import pygame
from constants import SCREENWIDTH, SCREENHEIGHT, BLACK, WHITE
from pygame.locals import *
from text import TextGroup

class PauseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 36)
        self.options = ["Resume", "Back to Title"]
        self.selected = 0
        self.textgroup = TextGroup()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key in [K_RETURN, K_KP_ENTER]:
                        return self.options[self.selected]
            self.draw()

    def draw(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("PAUSED", True, WHITE)
        self.screen.blit(title_text, ((SCREENWIDTH - title_text.get_width()) // 2, 100))

        for idx, option in enumerate(self.options):
            color = WHITE
            if idx == self.selected:
                color = (255, 0, 0)  # Highlight color
            option_text = self.font.render(option, True, color)
            self.screen.blit(option_text, ((SCREENWIDTH - option_text.get_width()) // 2, 250 + idx * 60))
        pygame.display.flip()