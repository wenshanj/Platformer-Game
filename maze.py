import pygame
import random

class Island(pygame.sprite.Sprite):
    def __init__(self,counter,row,col,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.counter = counter
        self.image = pygame.transform.scale(
            (pygame.image.load("maze/gemBlue.png").convert_alpha()),(40,40))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.isOccupied = False
        self.aiOccupied = False
    
    def update(self):
        if self.isOccupied == False:
            self.image = pygame.transform.scale(
            (pygame.image.load("maze/gemBlue.png").convert_alpha()),(40,40))
        if self.aiOccupied == True:
            self.image = pygame.transform.scale(
            (pygame.image.load("maze/gemYellow.png").convert_alpha()),(40,40))
        if self.counter == 0 or self.isOccupied == True:
            self.image = pygame.transform.scale(
            (pygame.image.load("maze/gemGreen.png").convert_alpha()),(40,40))

class Rod(pygame.sprite.Sprite):
    def __init__(self,direction,row,col,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.row = col
        self.col = row
        self.direction = direction
        if self.direction == "East" or self.direction == "West":
            self.image = pygame.Surface((50,5))
        else:
            self.image = pygame.Surface((5,50))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        if self.direction == "North":
            self.rect.midbottom = (self.x,self.y)
        elif self.direction == "South":
            self.rect.midtop = (self.x,self.y)
        elif self.direction == "East":
            self.rect.midleft = (self.x,self.y)
        else:
            self.rect.midright = (self.x,self.y)
