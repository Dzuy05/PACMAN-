import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData
from hand import HandController
from direction_handler import process_hand_direction
from screen import TitleScreen
from option import OptionScreen  
from sprites import Spritesheet  
import settings
import sys
import os
import json
import pygetwindow as gw
from tutoscreen import TutorialScreen

HIGH_SCORES_FILE = "high_scores.json"

def load_high_scores():
    if not os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'w') as f:
            json.dump([], f)
    with open(HIGH_SCORES_FILE, 'r') as f:
        return json.load(f)

def save_high_scores(high_scores):
    with open(HIGH_SCORES_FILE, 'w') as f:
        json.dump(high_scores, f, indent=4)

def showScoreScreen(screen, score):
    pygame.font.init()
    font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    large_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
    clock = pygame.time.Clock()
    user_text = ''
    active = False
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    input_box = pygame.Rect(SCREENWIDTH//2 - 100, SCREENHEIGHT//2, 200, 50)
    done = False
    submitted = False

    try:
        background = pygame.image.load(os.path.join("2.png")).convert()
        background = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
    except pygame.error as e:
        background = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if user_text.strip() == '':
                            user_text = 'Player'
                        high_scores = load_high_scores()
                        high_scores.append({"name": user_text, "score": score})
                        high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)
                        high_scores = high_scores[:7]
                        save_high_scores(high_scores)
                        submitted = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        if not submitted:
            score_surf = large_font.render(f"Your Score: {score}", True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(SCREENWIDTH//2, SCREENHEIGHT//2 - 100))
            screen.blit(score_surf, score_rect)

            pygame.draw.rect(screen, color, input_box, 2)

            text_surf = font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surf, (input_box.x+5, input_box.y+10))

            prompt_surf = font.render("Enter your name and press Enter:", True, (255, 255, 255))
            prompt_rect = prompt_surf.get_rect(center=(SCREENWIDTH//2, SCREENHEIGHT//2 - 50))
            screen.blit(prompt_surf, prompt_rect)
        else:
            high_scores = load_high_scores()

            title_surf = large_font.render("High Scores", True, (255, 215, 0))
            title_rect = title_surf.get_rect(center=(SCREENWIDTH//2, SCREENHEIGHT//2 - 150))
            screen.blit(title_surf, title_rect)

            for idx, entry in enumerate(high_scores):
                name = entry['name']
                entry_score = entry['score']
                entry_text = f"{idx + 1}. {name}: {entry_score}"
                entry_surf = font.render(entry_text, True, (255, 255, 255))
                entry_rect = entry_surf.get_rect(center=(SCREENWIDTH//2, SCREENHEIGHT//2 - 100 + idx * 40))
                screen.blit(entry_surf, entry_rect)

            back_surf = font.render("Press ESC to return to Main Menu", True, (255, 255, 255))
            back_rect = back_surf.get_rect(center=(SCREENWIDTH//2, SCREENHEIGHT//2 + 220))
            screen.blit(back_surf, back_rect)

        pygame.display.flip()
        clock.tick(30)

        if submitted:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                done = True

class GameController(object):
    def __init__(self, skin="Pacman"):
        self.skin = skin
        self.spritesheet = Spritesheet(theme=self.skin)  
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENRES, 0)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()
        self.hand = HandController()
        self.running = True
        self.gameplay_surface = pygame.surface.Surface(SCREENSIZE).convert()
        
        self.offset = ((SCREENRES[0] - SCREENWIDTH) // 2, (SCREENRES[1] - SCREENHEIGHT) // 2)
        if not os.path.exists("highscores.txt"):
            with open("highscores.txt", "w") as file:
                file.write("# Điểm số sẽ được thêm vào dưới dạng 'Tên: Điểm số'\n")

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENRES).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENRES).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):      
        self.hand.start()

        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)

        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

        while self.running:
            self.update()

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)      
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

            hand_direction = self.hand.get_direction()
            keyboard_direction = self.pacman.getValidKey()

            if keyboard_direction is not None:
                self.pacman.set_desired_direction(keyboard_direction)
            elif hand_direction is not None:
                self.pacman.set_desired_direction(hand_direction)

            self.pacman.update(dt)

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def goBackToTitle(self):
        self.running = False

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.hand.stop()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSESCTXT)
                            self.hideEntities()
                elif event.key == K_ESCAPE:
                    self.goBackToTitle()    
                elif event.key == K_ESCAPE:
                    self.goBackToTitle()
                elif event.key == K_t:  
                    self.hand.toggle_camera()
    

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)                  
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()               
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.endGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def endGame(self):
        self.hand.stop()
        showScoreScreen(self.screen, self.score)
        self.running = False

    def restartToTitle(self):
        self.hand.stop()
        pygame.quit()
        import subprocess
        subprocess.call([sys.executable] + sys.argv)
        sys.exit()

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.textgroup.updateLevel(self.level)
        self.startGame()

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREENRES, 0, 32)
    pygame.display.set_caption('PACMAN')
    logo = pygame.image.load('pacman.png')
    pygame.display.set_icon(logo)
    pygame.mixer.init()
    try:
            pygame.mixer.music.load(os.path.join("pac.mp3"))
            pygame.mixer.music.set_volume(0)
            pygame.mixer.music.play(-1)  
    except pygame.error:
            pass
    
    while True:
        title_screen = TitleScreen(screen)
        selection = title_screen.run()  
        if selection == "START":
            
            game = GameController(skin=settings.get_theme())
            game.startGame()
            while game.running:
                game.update()
        elif selection == "OPTION":
            option_screen = OptionScreen(screen)
            option_selection = option_screen.run()
        elif selection == "TUTORIAL":
            tutorial_screen = TutorialScreen(screen)
            tutorial_screen.run()
        elif selection == "EXIT":
            pygame.quit()
            exit()