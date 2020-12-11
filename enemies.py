import pygame
import random

class Slime(pygame.sprite.Sprite): 
    typeImageList = ["enemies/slimePink_walk.png","enemies/slimeGreen_walk.png","enemies/slimeBlue_walk.png"]
    squashedList = ["enemies/slime_squashed.png","enemies/slimeGreen_squashed.png","enemies/slimeBlue_squashed.png"]
    deadList = ["enemies/slime_dead.png","enemies/slimeGreen_dead.png","enemies/slimeBlue_dead.png"]

    def __init__(self,col,borderLeft,borderRight):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.index = (random.randint(0,2))
        self.image = pygame.transform.scale(
            (pygame.image.load(Slime.typeImageList[self.index]).convert_alpha()),(43,30))
        self.borderLeft = borderLeft
        self.borderRight = borderRight
        self.rect = self.image.get_rect()
        self.initX = random.randint((col-4)*50,(col-3)*50)
        self.rect.midbottom = (self.initX, 400)
        self.dirx = random.randint(-9,-6)      #random speed
        self.isSquashed = False
        self.isDead = False
        self.isHit = False
        self.timer = 0


    def motionAnimation(self):
        self.rect.x += self.dirx
        if self.rect.left < self.borderLeft:          
            self.rect.left = self.borderLeft
            self.image = pygame.transform.flip(self.image, True, False)
            self.dirx = -self.dirx
        elif self.rect.right > self.borderRight:
            self.rect.right = self.borderRight
            self.image = pygame.transform.flip(self.image, True, False)
            self.dirx = -self.dirx

    def update(self):
        self.motionAnimation()
        if self.isHit == True:
            self.image = pygame.transform.scale(
                (pygame.image.load("enemies/slime_hit.png").convert_alpha()),(43,30))
            if self.dirx > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.timer += 1
            self.dirx = 0
            self.isDead = True
        if self.isSquashed == True:
            if self.dirx < 0:
                self.image = pygame.transform.scale(
                (pygame.image.load(Slime.deadList[self.index]).convert_alpha()),(43,30))
            if self.dirx > 0:
                self.image = pygame.transform.scale(
                (pygame.image.load(Slime.deadList[self.index]).convert_alpha()),(43,30))
                self.image = pygame.transform.flip(self.image, True, False)
            self.dirx = 0
            self.isDead = True
            self.timer += 1
        if self.timer == 5 or (abs(self.borderRight) - abs(self.borderLeft) < 100):
            self.kill()

class FlyMan(pygame.sprite.Sprite):
    def __init__(self,col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            (pygame.image.load("enemies/flyMan_fly.png").convert_alpha()),(50,62))
        self.rect = self.image.get_rect()
        #self.initX = random.randint((col-4)*50,(col-3)*50)
        self.rect.center = (800, 105)
        self.timer = 0
        self.lightingGenerated = 0
        self.isDead = False

    def update(self):
        if self.isDead:
            self.kill()

class Lighting(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            (pygame.image.load("enemies/lighting_yellow.png").convert_alpha()),(30,80))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y)
        self.speed = 13
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > 400:
            self.kill()