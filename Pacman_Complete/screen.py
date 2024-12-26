import pygame
from constants import SCREENWIDTH, SCREENHEIGHT, BLACK, WHITE
from pygame.locals import *
import os
import sys
import time
import cv2
from hand_screen import detect_gesture
import mediapipe as mp

mp_hands = mp.solutions.hands

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font("PressStart2P-Regular.ttf", 64)
        self.option_font = pygame.font.Font("PressStart2P-Regular.ttf", 32)
        self.options = ["START", "TUTORIAL", "OPTION", "EXIT"]
        self.selected = 0

        self.background = pygame.image.load(os.path.join("3.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREENWIDTH, SCREENHEIGHT))

        self.blink = True
        self.last_blink_time = time.time()
        self.blink_interval = 0.5

        self.cap = None
        self.last_gesture = None

    def get_hand_gesture(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            result = hands.process(rgb_frame)
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    gesture = detect_gesture(hand_landmarks, width, height)
                    return gesture
        return None

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for idx, option in enumerate(self.options):
            if idx == self.selected:
                color = (255, 215, 0) 
            else:
                color = WHITE

            option_surface = self.option_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 20 + idx * 50))
            self.screen.blit(option_surface, option_rect)

        pygame.display.flip()

    def run(self):
        self.cap = cv2.VideoCapture(0)  
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            gesture = self.get_hand_gesture()
            if gesture != self.last_gesture:
                if gesture == "1":
                    self.selected = (self.selected - 1) % len(self.options)
                elif gesture == "2":
                    self.selected = (self.selected + 1) % len(self.options)
                elif gesture == "FIST":
                    return self.options[self.selected]
                self.last_gesture = gesture

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == K_RETURN or event.key == K_SPACE:
                        self.cap.release()
                        cv2.destroyAllWindows()
                        return self.options[self.selected]
            self.draw()
