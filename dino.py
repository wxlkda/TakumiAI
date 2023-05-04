import pygame, sys, os
from pygame.locals import *
from constants import *

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 2.0

    def __init__(self):
        self.dino_run = True
        self.dino_jump = False
        self.state = "idle"
        #self.shadow = [pygame.Rect(self.rect.x + 3, self.rect.bottom - 3, size[0] * 0.75, 3.5), pygame.Rect(self.rect.x + 5, self.rect.bottom - 2, size[0] * 0.75, 3.5)]
        self.frames = {"idle": [pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/Assets/Character/adventurer-idle-2-0{i}.png"), (100, 74)) for i in range(4)],
                       "run": [pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/Assets/Character/adventurer-run-0{i}.png"), (100, 74)) for i in range(6)],
                       "dead": [pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/Assets/Character/adventurer-die-0{i}.png"), (100, 74)) for i in range(7)],
                       "jump-up":  [pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/Assets/Character/adventurer-jump-0{i}.png"), (100, 74)) for i in range(4)]}
        self.image = pygame.transform.scale(pygame.image.load(f"{os.path.dirname(__file__)}/Assets/Character/adventurer-idle-2-00.png"), (100, 74))
        self.millisec_rate = {"idle": 200, "run" : 1000 // 10, "dead" : 1000 // 15, "jump-up": 1000 // 13}# inter-frame delay in milliseconds
        self.current_frame = {"idle": 0, "run" : 0, "dead" : 0, "jump-up": 0}
        self.last_frame_at = {"idle": 0, "run" : 0, "dead" : 0, "jump-up": 0}

        self.jump_vel = self.JUMP_VEL
        self.image = self.frames["run"][0]
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, 23 * 2, 27 * 2)
        self.grounded = True

    def update(self, userInput = None):
        self.animate()
        if not userInput:
            return
        if self.rect.y >= 310:
            self.grounded = True
        else:
            self.grounded = False
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump and self.grounded:
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_jump = False

    def animate(self):
        time_now = pygame.time.get_ticks()
        if (time_now > self.last_frame_at[self.state] + self.millisec_rate[self.state]):
            self.last_frame_at[self.state] = time_now
            self.current_frame[self.state] += 1
            if (self.current_frame[self.state] == len( self.frames[self.state] ) ):
                if self.state in ["jump-up"]:
                    self.current_frame[self.state] = len(self.frames[self.state]) - 1
                else:
                    self.current_frame[self.state] = 0
            self.image = self.frames[self.state][self.current_frame[self.state]]

    def run(self):
        self.state = "run"
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS

    def jump(self):
        self.state = "jump-up"
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.1
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 34, self.rect.y - 19))
