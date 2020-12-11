import pygame
import random

class Player(pygame.sprite.Sprite):
    brownBunnyActionList = ["player/bunny1_stand.png", "player/bunny1_walk1.png",
    "player/bunny1_jump.png", "player/bunny1_walk2.png"]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.isStanding = True
        self.landOnTile = False
        self.isJumping = False
        self.isMovingRight = False
        self.projectileMotion = False
        self.isFalling = False
        self.coinCount = 0
        self.health = 2
        self.bulletNumber = 2
        self.isHurt = False
        self.image = pygame.transform.scale(
            (pygame.image.load(Player.brownBunnyActionList[0]).convert_alpha()),(55,90))
        self.walkingIndex = 1
        self.rect = self.image.get_rect()
        self.rect.center = (100,350)        #set initial position
        self.velocityY = 0
        self.velocityX = 0
        self.gravity = 0
        self.timer = 0
        self.timerGame = 120
        self.score = 0
        self.startJumping = False

    def keyPress(self):
        self.gravity = 2
        self.velocityX = 0

        self.isStanding = True
        self.isMovingRight = False 
        self.landOnTile = False

        if self.isHurt == False:
            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_LEFT]:
                self.velocityX = -7
                self.isStanding = False
            
            if keyPressed[pygame.K_RIGHT]:
                self.velocityX  = 7
                self.isStanding = False
                self.isMovingRight = True
            
            if keyPressed[pygame.K_UP] and self.velocityY == 0:
                self.startJumping = True
            
            if keyPressed[pygame.K_UP]:
                self.isJumping = True
                self.velocityY = -10
                self.projectileMotion = False
                self.isStanding = False
            
        
            if ((keyPressed[pygame.K_UP] and keyPressed[pygame.K_LEFT]) or
            (keyPressed[pygame.K_UP] and keyPressed[pygame.K_RIGHT])):
                self.projectileMotion = True
        
            self.rect.x += self.velocityX
            self.velocityY += self.gravity
            self.rect.y += self.velocityY

    def motionAnimation(self):
        if self.isStanding == False or self.projectileMotion == True:
            self.walkingIndex= -self.walkingIndex
            self.image = pygame.transform.scale(
            (pygame.image.load(Player.brownBunnyActionList[self.walkingIndex]).convert_alpha()),(55,90))
            if self.isMovingRight == False:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.isStanding == True:
            self.image = pygame.transform.scale(
                (pygame.image.load(Player.brownBunnyActionList[0]).convert_alpha()),(55,90))
        if self.isJumping == True and self.projectileMotion == False:
            self.image = pygame.transform.scale(
                (pygame.image.load(Player.brownBunnyActionList[2]).convert_alpha()),(65,81))    

    def update(self):
        self.keyPress()
        self.motionAnimation()
        if self.isHurt == True:
            self.image = pygame.transform.scale(
            (pygame.image.load("player/bunny1_hurt.png").convert_alpha()),(70,90))
            self.timer += 1
        if self.timer == 20:
            self.isHurt = False
            self.timer = 0 
        if self.health == 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,posX,posY,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            (pygame.image.load("player/carrot.png").convert_alpha()),(30,22))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = posX
        self.rect.y = posY
        self.speed = speed
        self.speedX = self.x/self.speed
        self.speedY = self.y/self.speed
        
    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if self.rect.left > 800 or self.rect.right < 0 or self.rect.top < 0 or self.rect.bottom > 800:
            self.kill()