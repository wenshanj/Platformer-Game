import pygame
import random

class Tile(pygame.sprite.Sprite):
    tileMap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 9, 0, 0, 0, 0, 0, 0, 29, 0, 0, 0, 0, 0, 9, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 29, 0, 10, 0, 29, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 10, 0, 9, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 29, 29, 29, 0, 0, 0, 0, 29, 29, 0, 0, 0, 0, 0, 0, 29, 0, 0, 0, 0, 0, 0, 0, 29, 29, 0, 0, 0, 0, 0, 29, 29, 29, 29, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 29, 29, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 29, 0, 0, 0, 0, 7, 6, 6, 6, 8, 0, 0, 29, 0, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0, 29, 0, 0, 0, 7, 6, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 29, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 27, 18, 22, 0],
               [0, 13, 23, 23, 0, 0, 0, 19, 23, 0, 0, 0, 0, 0, 23, 14, 23, 0, 0, 0, 0, 0, 15, 20, 0, 0, 0, 0, 24, 24, 0, 0, 0, 19, 20, 0, 0, 14, 0, 0, 24, 24, 24, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 14, 0, 23, 23, 23, 0, 0, 0, 19, 0, 0, 0, 0, 0, 12, 0, 26, 28, 17, 21, 0],
               [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 3, 2, 2, 2, 2, 4, 0, 0, 3, 2, 2, 4, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]

    def __init__(self,row,col,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            (pygame.image.load(image).convert_alpha()),(50,50))
        self.rect = self.image.get_rect() 
        self.rect.x = col*50
        self.rect.y = row*50

class Coin(pygame.sprite.Sprite):
    motionImageList = ["background/gold_1.png","background/gold_2.png","background/gold_3.png","background/gold_4.png"]

    def __init__(self,row,col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.i = 0
        self.increment = 1
        self.image = pygame.transform.scale(
                (pygame.image.load(Coin.motionImageList[self.i]).convert_alpha()),(35,35))
        self.rect = self.image.get_rect() 
        self.rect.x = col*50
        self.rect.y = row*50
    
    def motion(self):
        if self.i == 0:
            self.increment = 1
        elif self.i == 3:
            self.increment = -1
        self.i += self.increment
        if self.i == 0:
            self.image = pygame.transform.scale(
                (pygame.image.load(Coin.motionImageList[self.i]).convert_alpha()),(35,35))
        elif self.i == 1:
            self.image = pygame.transform.scale(
                (pygame.image.load(Coin.motionImageList[self.i]).convert_alpha()),(36,35))
        elif self.i == 2:
            self.image = pygame.transform.scale(
                (pygame.image.load(Coin.motionImageList[self.i]).convert_alpha()),(25,35))
        elif self.i == 3:
            self.image = pygame.transform.scale(
                (pygame.image.load(Coin.motionImageList[self.i]).convert_alpha()),(10,35))

    def update(self):
        self.motion()

class Box(pygame.sprite.Sprite):
    #boxType (0) = Item,     boxType(1) = Explosive
    def __init__(self,row,col,boxType):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.type = boxType
        if self.type == 0:
            self.image = pygame.transform.scale(
                (pygame.image.load("background/boxItemAlt.png").convert_alpha()),(50,50))
        else:
            self.image = pygame.transform.scale(
                (pygame.image.load("background/boxExplosive.png").convert_alpha()),(50,50))
        self.rect = self.image.get_rect() 
        self.rect.x = col*50
        self.rect.y = row*50
        self.collide = False
        self.dropItem = False
    
    def collisionImage(self):
        if self.collide == True:
            if self.type == 0:
                self.image = pygame.transform.scale(
                (pygame.image.load("background/boxItemAlt_disabled.png").convert_alpha()),(50,50))
            else:
                self.image = pygame.transform.scale(
                (pygame.image.load("background/boxExplosive_disabled.png").convert_alpha()),(50,50))

    def update(self):
        self.collisionImage()

class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,boxType,randomNum):
        pygame.sprite.Sprite.__init__(self)
        self.type = boxType
        self.x = x
        self.y = y
        self.randomNum = randomNum
        if self.type == 0:
            if self.randomNum == 0:
                self.image = pygame.transform.scale(
                    (pygame.image.load("background/lifes.png").convert_alpha()),(30,35))
            else:
                self.image = pygame.transform.scale(
                (pygame.image.load("background/carrots.png").convert_alpha()),(30,30))
        else:
            self.image = pygame.transform.scale(
                (pygame.image.load("background/bomb.png").convert_alpha()),(40,40))
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.x,self.y)
        self.speed = 20
        self.timer = 0
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom >= 400:
            self.rect.bottom = 400
            if self.type == 1:
                self.image = pygame.transform.scale(
                    (pygame.image.load("background/bombFlash.png").convert_alpha()),(40,40))
            self.timer += 1
        if self.timer == 9:
            self.kill()

class Icons(pygame.sprite.Sprite):
    def __init__(self,x,y,iconType):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.iconType = iconType
        if self.iconType == "live":
            self.image = pygame.transform.scale(
                (pygame.image.load("background/lifes.png").convert_alpha()),(25,35))
        elif self.iconType == "bullet":
            self.image = pygame.transform.scale(
                (pygame.image.load("background/carrots.png").convert_alpha()),(25,25))
        else:
            self.image = pygame.transform.scale(
                (pygame.image.load("background/coin_gold.png").convert_alpha()),(25,25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y