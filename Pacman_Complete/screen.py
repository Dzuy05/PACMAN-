import pygame
from constants import SCREENWIDTH, SCREENHEIGHT, BLACK, WHITE
from pygame.locals import *
import os
import sys

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("PressStart2P-Regular.ttf", 64)
        self.option_font = pygame.font.Font("PressStart2P-Regular.ttf", 32)
        self.options = ["START", "OPTION", "EXIT"]
        self.selected = 0

        self.background = pygame.image.load(os.path.join("3.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREENWIDTH, SCREENHEIGHT))

        pygame.mixer.init()
        try:
            pygame.mixer.music.load(os.path.join("pac.mp3"))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)  
        except pygame.error:
            print("Background music file not found or unsupported format.")

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for idx, option in enumerate(self.options):
            if idx == self.selected:
                color = (255, 215, 0)  
            else:
                color = WHITE

            option_surface = self.option_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 + idx * 60))
            self.screen.blit(option_surface, option_rect)

        pygame.display.flip()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)  
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    pygame.mixer.music.stop()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == K_RETURN or event.key == K_SPACE:
                        return self.options[self.selected]
            self.draw()