from constants import *
from pacman import Pacman

def process_hand_direction(hand_direction, pacman: Pacman):
    if hand_direction and pacman.validDirection(hand_direction):
        pacman.set_desired_direction(hand_direction)
