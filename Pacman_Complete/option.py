# FILE: option_screen.py

import pygame
from constants import SCREENWIDTH, SCREENHEIGHT, BLACK, WHITE
from pygame.locals import *
import settings  
import os
import sys
import time

class OptionScreen:
    def __init__(self, screen):
        self.screen = screen
        # Load custom fonts
        self.title_font = pygame.font.Font("PressStart2P-Regular.ttf", 64)
        self.option_font = pygame.font.Font("PressStart2P-Regular.ttf", 32)
        self.options = ["PACMAN", "PACMAN 3", "BACK"] 
        self.selected = 0

        self.background = pygame.image.load(os.path.join("2.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREENWIDTH, SCREENHEIGHT))

        self.blink = True
        self.last_blink_time = time.time()
        self.blink_interval = 0.5  # Seconds

        self.option_indicators = {}

        for option in self.options:
            if option != "BACK":
                left_indicator_path = f"{option.lower().replace(' ', '_')}_left.png"
                right_indicator_path = f"{option.lower().replace(' ', '_')}_right.png"

                self.option_indicators[option] = {
                    "left": pygame.image.load(os.path.join(left_indicator_path)).convert_alpha(),
                    "right": pygame.image.load(os.path.join(right_indicator_path)).convert_alpha()
                }

                # Resize indicators if needed
                indicator_scale = 1  # Adjust scale if necessary
                left_image = self.option_indicators[option]["left"]
                right_image = self.option_indicators[option]["right"]

                self.option_indicators[option]["left"] = pygame.transform.scale(
                    left_image,
                    (int(left_image.get_width() * indicator_scale),
                     int(left_image.get_height() * indicator_scale))
                )
                self.option_indicators[option]["right"] = pygame.transform.scale(
                    right_image,
                    (int(right_image.get_width() * indicator_scale),
                     int(right_image.get_height() * indicator_scale))
                )

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        current_time = time.time()
        if current_time - self.last_blink_time >= self.blink_interval:
            self.blink = not self.blink
            self.last_blink_time = current_time

        starting_y = SCREENHEIGHT // 2 - 100  

        option_spacing = 150  

        for idx, option in enumerate(self.options):
            option_surface = self.option_font.render(option, True, WHITE)
            option_rect = option_surface.get_rect(center=(SCREENWIDTH // 2, starting_y + idx * option_spacing))

            if idx == self.selected:
                color = (255, 215, 0) 
                if self.blink:
                    option_surface = self.option_font.render(option, True, color)
                    self.screen.blit(option_surface, option_rect)

                    if option != "BACK":
                        left_indicator = self.option_indicators[option]["left"]
                        right_indicator = self.option_indicators[option]["right"]

                        left_indicator_rect = left_indicator.get_rect(
                            center=(
                                option_rect.left - left_indicator.get_width() // 2 - 10,
                                option_rect.centery
                            )
                        )
                        right_indicator_rect = right_indicator.get_rect(
                            center=(
                                option_rect.right + right_indicator.get_width() // 2 + 10,
                                option_rect.centery
                            )
                        )

                        self.screen.blit(left_indicator, left_indicator_rect)
                        self.screen.blit(right_indicator, right_indicator_rect)
                else:
                    pass
            else:
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
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key in (K_RETURN, K_KP_ENTER):
                        selected_option = self.options[self.selected]
                        if selected_option == "BACK":
                            return "Back"
                        else:
                            settings.set_theme(selected_option)
                            return selected_option.upper()
            self.draw()
