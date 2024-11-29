import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.speed = 80
        self.sprites = PacmanSprites(self)
        self.desired_direction = STOP

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
        self.speed = 80

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        
        if self.overshotTarget():
            self.node = self.target
            self.setPosition()

            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
                self.setPosition()

            valid_directions = self.getValidDirections()
            if self.desired_direction in valid_directions:
                self.direction = self.desired_direction
            elif self.direction not in valid_directions:
                self.direction = STOP

            self.target = self.getNewTarget(self.direction)
        else:
            if self.desired_direction == self.direction * -1:
                self.direction = self.desired_direction
                self.reverseDirection()

    def set_desired_direction(self, direction):
        self.desired_direction = direction

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        elif key_pressed[K_DOWN]:
            return DOWN
        elif key_pressed[K_LEFT]:
            return LEFT
        elif key_pressed[K_RIGHT]:
            return RIGHT
        else:
            return None  

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
