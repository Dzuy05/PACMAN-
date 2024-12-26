import pygame, sys, os
from constants import SCREENWIDTH, SCREENHEIGHT, WHITE
from pygame.locals import *
import cv2
import mediapipe as mp
from hand_screen import detect_gesture
import time

mp_hands = mp.solutions.hands

class TutorialScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 15)
        self.background = pygame.image.load(os.path.join("2.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREENWIDTH, SCREENHEIGHT))
        self.options = ["BACK"]
        self.selected = 0

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
        tutorial_text = [
            "Hand ups to move up",
            "Hand down to move down",
            "Similar with left and right",
            "Press ESC to return to the main menu."
        ]
        for idx, line in enumerate(tutorial_text):
            text_surface = self.font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 100 + idx * 50))
            self.screen.blit(text_surface, text_rect)
        

        for idx, option in enumerate(self.options):
            color = WHITE
            if idx == self.selected:
                color = (255, 215, 0)  
            option_surface = self.font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 + 150))
            self.screen.blit(option_surface, option_rect)

        pygame.display.flip()

    def run(self):
        self.cap = cv2.VideoCapture(0)
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)
            #gesture = self.get_hand_gesture()
            #if gesture != self.last_gesture:
                #if gesture == "FIST":
                    #return self.options[self.selected]
                #self.last_gesture = gesture

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key in (K_SPACE, K_RETURN):
                        if self.options[self.selected] == "BACK":
                            running = False
            self.draw()