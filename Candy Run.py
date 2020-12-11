import pygame
import random
from player import*
from enemies import*
from background import*
from maze import*

#Graphics attribute to @janachumi(UI) and Kenney Vleugels from OpenGameArt
#Followed YouTuber KidsCanCode for pygame tutorial for creating spritie classes
#Font SunnyCloudy.ttf is by Nur Solikh from dafont
#Font Bubble Bobble.ttf is by Almarkhatype Studio from dafont
#Font PWYummyDonuts.ttf is by Peax Webdesign from dafont
#Chip song and Pickup_Coin sound effect by bart from openGameArt.org
#Click, click2 and negative sound effect by Lokif from openGameArt.org
#Bomb sound effect by Luke.RUSTLTD from openGameArt.org
#Beep, coin, and misc sound effect by rubberduck from openGameArt.org
#Shoot, collect_Point, win, and lose sound effect by Little Robot Sound Factory, and provide this link where possible: www.littlerobotsoundfactory.com
#Jump sound effect: Boing Raw Copyright 2005 cfork <http://freesound.org/people/cfork/> Boing Jump Copyright 2012 Iwan Gabovitch <http://qubodup.net>
#Death sound effect by sauer2 from openGameArt.org
#Intro Theme by CodeMenu from openGameArt.org

#Framework adopted from Lukas Peraza
#http://blog.lukasperaza.com/getting-started-with-pygame/
class PygameGame(object):
    def __init__(self, width=800, height=500, fps=50, title="Candy Run!"):
        pygame.init()
        pygame.mixer.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.mode = "main"

        #sound init
        self.menuSong = pygame.mixer.Sound("sound effect/chip song.ogg")
        self.coinSound = pygame.mixer.Sound("sound effect/Pickup_Coin.wav")
        self.clickSound = pygame.mixer.Sound("sound effect/click.wav")
        self.clickSound2 = pygame.mixer.Sound("sound effect/click_2.wav")
        self.shotSound = pygame.mixer.Sound("sound effect/Shoot.wav")
        self.successPurchase = pygame.mixer.Sound("sound effect/Collect_Point.wav")
        self.failedPurchase = pygame.mixer.Sound("sound effect/negative.wav")
        self.enemiesDieSound = pygame.mixer.Sound("sound effect/misc.wav")
        self.boxHitSound = pygame.mixer.Sound("sound effect/coin.wav")
        self.explosionSound = pygame.mixer.Sound("sound effect/explosion.wav")
        self.collectItemSound = pygame.mixer.Sound("sound effect/beep.wav")
        self.jumpSound = pygame.mixer.Sound("sound effect/jump.wav")
        self.hurtSound = pygame.mixer.Sound("sound effect/death.wav")
        self.gameOverSound = pygame.mixer.Sound("sound effect/lose.ogg")
        self.gameWonSound = pygame.mixer.Sound("sound effect/win.ogg")
        self.mazeSong = pygame.mixer.Sound("sound effect/Intro Theme.ogg")
        self.themeSongPlaying = False

        #login init
        self.userName = ""
        self.password = ""
        self.enterUserName = False
        self.enterPassword = False
        self.errorMsg = False
        self.purchaseFailed = None
        self.addStat = False

        #maze init
        self.border = 25
        self.allIslands = pygame.sprite.Group()
        self.allRods = pygame.sprite.Group()
        self.mazeDict = {}
        self.visited = []
        self.counter = 0
        self.start = 0
        self.end = 159
        self.currIsland = 0
        self.playerVisted = set()
        self.playerVisted.add(0)
        self.mazeTimer = 0

        #game init
        self.background = pygame.transform.scale(
            (pygame.image.load("background/background.png").convert_alpha()),(1000,500))
        self.backgroundX = 0
        self.backgroundX2 = self.background.get_width()
        self.scrollValue = 0
        self.isCameraMoving = None
        self.coinEatenList = []
        self.boxHitList = []
        self.font = "font/SunnyCloudy.ttf"
        self.directionFont = "font/Bubble Bobble.ttf"
        self.titleFont = "font/PWYummyDonuts.ttf"
        self.slimeTenCreated = False
        self.slimeFortyFourCreated = False
        self.slimeSixtyFiveCreated = False
        self.flyManSeventeenCreated = False
        self.flyManFortyCreated = False
        self.flyManSixtyFiveCreated = False
        self.timeUsed = 0
        self.playerHitItem = False

        #Enemies, Player, Bullets
        self.allSprites = pygame.sprite.Group()
        self.allSlimes = pygame.sprite.Group()
        self.allFlyMan = pygame.sprite.Group()
        self.allBullets = pygame.sprite.Group()
        self.allLighting = pygame.sprite.Group()
        self.player = (Player())
        self.allSprites.add(self.player)
        self.allIcons = pygame.sprite.Group()
        self.endGoal = pygame.sprite.Group()

        #Tiles, decor, coin, mystery boxes
        self.allPlatforms = pygame.sprite.Group()
        self.allTilesNotFloor = pygame.sprite.Group()
        self.tileDecor = pygame.sprite.Group()
        self.allCoins = pygame.sprite.Group()
        self.allOcean = pygame.sprite.Group()
        self.allBoxes = pygame.sprite.Group()
        self.boxHitGroup = pygame.sprite.Group()
        self.boxItemDrop = pygame.sprite.Group()

    #Plays the main sound indefinitely
    def playSong(self):
        if self.mode == "main" and self.themeSongPlaying == False:
            self.menuSong.play(-1)
            self.themeSongPlaying = True
    
    #Control user point of view with respect to the screen
    def camera(self):
        centerX = self.player.rect.center[0]
        if self.player.velocityX != 0 and self.player.rect.right > 300:
            if self.player.velocityX > 0:
                self.scrollValue += self.player.velocityX+12
            else:
                self.scrollValue += self.player.velocityX+7
            if self.scrollValue > 2900:
                self.scrollValue = 2900
            self.isCameraMoving = True
    
    #Help to give the background movement that's independent from the player
    #Citation: https://techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/background/
    def backgroundScrolling(self):
        if self.player.velocityX != 0:
            self.backgroundX -= 3
            self.backgroundX2 -= 3
        if self.backgroundX < self.background.get_width() * -1:
            self.backgroundX = self.background.get_width()
        if self.backgroundX2 < self.background.get_width() * -1:
            self.backgroundX2 -= self.background.get_width()

    #Detect the collision between player and tiles, help player stands on the platform
    #Inspired by KidsCanCode at https://www.youtube.com/watch?v=pN9pBx5ln40 and 
    #and DaFluffyPotato at https://www.youtube.com/watch?v=HCWI2f7tQnY&t=615s
    def platformCollision(self):
        hits = pygame.sprite.spritecollide(self.player, self.allOcean, False)
        if hits:
            self.player.health = 0 
            self.player.kill()
        hits = pygame.sprite.spritecollide(self.player, self.allPlatforms, False)
        #if land on any tiles
        if self.player.velocityY > 0 and hits:
            self.player.rect.bottom == hits[0].rect.top
            self.player.velocityY = 0
            self.player.isJumping = False
            self.player.landOnTile = True
            if hits[0].rect.top == 250:
                self.player.rect.bottom = 250
            if self.player.rect.y > 311:
                self.player.rect.y = 311

        #if jump and touches any tile
        if self.player.velocityY < 0 and hits:
            self.player.rect.top = hits[0].rect.bottom
            self.player.velocityY = 0
            self.playerHitItem = True

        #if jump and touches any other tiles other than floor
        hits = pygame.sprite.spritecollide(self.player, self.allTilesNotFloor, False)
        if hits and self.player.landOnTile == False:
            if self.player.velocityX >= 0:
                self.player.rect.right = hits[0].rect.left
            elif self.player.velocityX <= 0:
                self.player.rect.left = hits[0].rect.right

        if self.player.rect.left < 0:
            self.player.rect.left = 0
        elif self.player.rect.right > 800:
            self.player.rect.right = 800
        if self.player.rect.top < 120:
            self.player.rect.top = 120
 
    #Control collision between coins and player, delete the coin, update the score
    #and coin number, and play sounds
    def coinCollision(self):
        hits = pygame.sprite.spritecollide(self.player, self.allCoins, True)
        if hits:
            self.player.coinCount += 1
            self.coinEatenList.append((hits[0].col, hits[0].row))
            self.player.score += 5
            self.coinSound.play()

    #Control collision between boxes and player, init item drop from boxes, 
    #and control the effect those items have on players
    def boxCollision(self):
        #boxType (0) = Item,     boxType(1) = Explosive
        hits = pygame.sprite.spritecollide(self.player, self.allBoxes, False)
        self.playerHitItem = False
        if hits: 
            for box in hits:
                box.collide = True
                self.boxHitList.append((box.col, box.row))
                self.boxHitGroup.add(box)
                self.playerHitItem = True
                if box.dropItem == False:
                    self.boxHitSound.play()
                    randomNum = random.randint(0,1)
                    item = (Item(box.rect.x, box.rect.bottom, box.type, randomNum))
                    self.allSprites.add(item)
                    self.boxItemDrop.add(item)
                    box.dropItem = True
            if self.player.velocityY < 0:
                self.player.rect.top = hits[0].rect.bottom
                self.player.velocityY = 0
        for items in self.boxItemDrop:
            if items.type == 1 and items.rect.bottom == 400:
                self.explosionSound.play()
        hits = pygame.sprite.spritecollide(self.player, self.boxItemDrop, False)
        if hits:
            if hits[0].type == 1 and hits[0].rect.bottom == 400:
                self.player.health -= 1
                self.player.isHurt = True
                hits[0].kill()
            elif hits[0].type == 0 and hits[0].rect.bottom == 400:
                self.collectItemSound.play()
                if hits[0].randomNum == 0:
                    self.player.health += 1
                else:
                    self.player.bulletNumber += 1
                hits[0].kill()
        hits = pygame.sprite.spritecollide(self.player, self.endGoal, False)
        if hits:
            self.mode = "finish"
            self.gameWonSound.play()

    #Update the location of box hited by players with respect to player movement
    def boxHitUpdate(self):
        for boxes in self.boxHitGroup:
            boxes.rect.x = boxes.col*50 - self.scrollValue
    
    #Control player image and state after hit by enemies
    def playerGetHurt(self):
        hits = pygame.sprite.spritecollide(self.player, self.allSlimes, False)
        if self.player.velocityY > 0 and hits:
            if hits[0].isSquashed == False:
                self.player.score += 200
                self.enemiesDieSound.play()
            hits[0].isSquashed = True
        elif (self.player.velocityY <= 0 and hits and hits[0].isSquashed == False 
        and self.player.isHurt == False):
            self.player.isHurt = True
            self.hurtSound.play()
            self.player.health -= 1
        hits = pygame.sprite.spritecollide(self.player, self.allLighting, True)
        if hits:
            self.player.isHurt = True
            self.hurtSound.play()
            self.player.health -= 1

    #Draw the game icons on the top left corner
    def drawGameScreen(self):
        for icons in self.allIcons:
                icons.kill()
        x = 3
        y = 3
        for i in range (self.player.health):
            live = Icons(x,y,"live")
            x += 28
            self.allIcons.add(live)
        x = 3
        y = 42
        for i in range (self.player.bulletNumber):
            bullet = Icons(x,y,"bullet")
            x += 28
            self.allIcons.add(bullet)
        x = 3 
        y = 70
        coin = Icons(x,y,"coin")
        self.allIcons.add(coin)
        self.drawText(self.directionFont,f'x {(self.player.coinCount)}',25,35,70,(212,175,55))
        self.drawText(self.directionFont,f"Time: {int(self.player.timerGame)}",20,5,100,(212,175,55))
        self.drawText(self.directionFont,f"Score: {self.player.score} ",20,5,125,(212,175,55))

    #Draw texts 
    #Followed by KidsCanCode at https://www.youtube.com/watch?v=U8yyrpuplwc&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=10
    def drawText(self,fontType,text,size,x,y,color):
        font = pygame.font.Font(fontType,size)
        textSurface = font.render(text,True,color)
        rect = textSurface.get_rect()
        rect.x = x
        rect.y = y
        self.screen.blit(textSurface,(rect))

    #Update the state of enemies after hit by a bullet
    def bulletHitEnemies(self):
        for bullets in self.allBullets:
            hits = pygame.sprite.spritecollide(bullets, self.allSlimes, False)
            if hits and hits[0].isHit == False:
                bullets.kill()
                hits[0].isHit = True
                self.enemiesDieSound.play()
                self.player.score += 200
            hits = pygame.sprite.spritecollide(bullets, self.allFlyMan, False)
            if hits:
                bullets.kill()
                hits[0].isDead = True
                self.enemiesDieSound.play()
                self.player.score += 400

    #Draw the background tiles and platforms, generate enemies
    def tileDrawing(self):
        if self.isCameraMoving != False:
            for tiles in self.allPlatforms:
                tiles.kill()
            for tiles in self.allTilesNotFloor:
                tiles.kill()
            for tiles in self.tileDecor:
                tiles.kill()
            for coins in self.allCoins:
                coins.kill()
            for boxes in self.allBoxes:
                if boxes not in self.boxHitGroup:
                    boxes.kill()
            for slimes in self.allSlimes:
                slimes.borderLeft -= self.scrollValue
                slimes.borderRight = (slimes.col+1)*50 - self.scrollValue + 5
                if slimes.borderLeft < 0:
                    slimes.borderLeft = 0
                if slimes.borderRight < 50:
                    slimes.kill() 
            colStart = self.scrollValue // 50
            colEnd = colStart + 17
            for row in range (3,10):
                for col in range (colStart,colEnd):
                    if ((col == 10 and self.slimeTenCreated == False) or
                         (col == 44 and self.slimeFortyFourCreated == False) or 
                         (col == 65 and self.slimeSixtyFiveCreated == False)):
                            if col == 10:
                                self.slimeTenCreated = True
                                borderRight = (col+1)*50 - self.scrollValue
                                borderLeft = self.scrollValue
                                slime = (Slime(col,borderLeft,borderRight))
                                self.allSlimes.add(slime)
                                self.allSprites.add(slime)
                            elif col == 44:
                                self.slimeFortyFourCreated = True
                                borderRight = 800
                                borderLeft = 0
                                slime = (Slime(col,borderLeft,borderRight))
                                self.allSlimes.add(slime)
                                self.allSprites.add(slime)
                            else:
                                self.slimeSixtyFiveCreated = True
                                borderRight = 800
                                borderLeft = 0
                                slime = (Slime(col,borderLeft,borderRight))
                                self.allSlimes.add(slime)
                                self.allSprites.add(slime)
                    if ((col == 17 and self.flyManSeventeenCreated == False) or
                        (col == 40 and self.flyManFortyCreated == False) or
                        (col == 65 and self.flyManSixtyFiveCreated == False)):
                            flyMan = (FlyMan(col))
                            self.allFlyMan.add(flyMan)
                            if col == 17:
                                self.flyManSeventeenCreated = True
                            elif col == 40:
                                self.flyManFortyCreated = True
                            else:
                                self.flyManSixtyFiveCreated = True
                    if Tile.tileMap[row][col] == 1:
                        tile = (Tile(row,col,"background/cakeCenter.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 2:
                        tile = (Tile(row,col,"background/cakeMid.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 3:
                        tile = (Tile(row,col,"background/cakeLeft.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 4:
                        tile = (Tile(row,col,"background/cakeRight.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 5:
                        tile = (Tile(row,col,"background/liquidWater.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                        self.allOcean.add(tile)
                    elif Tile.tileMap[row][col] == 6:
                        tile = (Tile(row,col,"background/cakeHalfAltMid.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allTilesNotFloor.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 7:
                        tile = (Tile(row,col,"background/cakeHalfAltLeft.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allTilesNotFloor.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 8:
                        tile = (Tile(row,col,"background/cakeHalfAltRight.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allTilesNotFloor.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 9 or Tile.tileMap[row][col] == 10:
                        if (col,row) not in self.boxHitList:
                            if Tile.tileMap[row][col] == 9:
                                box = (Box(row,col,0))
                            else:
                                box = (Box(row,col,1))
                            box.rect.x -= self.scrollValue
                            self.allBoxes.add(box)
                    elif Tile.tileMap[row][col] == 11:
                        tile = (Tile(row,col,"background/boxAlt.png"))
                        tile.rect.x -= self.scrollValue
                        self.allPlatforms.add(tile)
                        self.allTilesNotFloor.add(tile)
                        self.allSprites.add(tile)
                    elif Tile.tileMap[row][col] == 12:
                        tile = (Tile(row,col,"background/signExit.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 13:
                        tile = (Tile(row,col,"background/signRight.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 14:
                        tile = (Tile(row,col,"background/cherry.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 15:
                        tile = (Tile(row,col,"background/canePink.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 16:
                        tile = (Tile(row,col,"background/canePinkTop.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 17:
                        tile = (Tile(row,col,"background/cupCake.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 18:
                        tile = (Tile(row,col,"background/creamPink.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 19:
                        tile = (Tile(row,col,"background/canePinkSmall.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 20:
                        tile = (Tile(row,col,"background/heart.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 21:
                        tile = (Tile(row,col,"background/lollipopBasePink.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 22:
                        tile = (Tile(row,col,"background/lollipopGreen.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 23:     
                        image = ["background/candyBlue.png", "background/candyYellow.png", 
                        "background/candyRed.png", "background/candyGreen.png"]
                        i = (random.randint(0,3))
                        tile = (Tile(row,col,image[i]))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 24:
                        image = ["background/waffleChoco.png", "background/wafflePink.png", 
                        "background/waffleWhite.png"]
                        i = (random.randint(0,2))
                        tile = (Tile(row,col,image[i]))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 25:
                        tile = (Tile(row,col,"background/hillCaneChocoTop.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 26:
                        tile = (Tile(row,col,"background/hillCaneChoco.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 27:
                        tile = (Tile(row,col,"background/lollipopFruitYellow.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                        self.endGoal.add(tile)
                    elif Tile.tileMap[row][col] == 28:
                        tile = (Tile(row,col,"background/lollipopBaseBrown.png"))
                        tile.rect.x -= self.scrollValue
                        self.tileDecor.add(tile)
                    elif Tile.tileMap[row][col] == 29:
                        if (col,row) not in self.coinEatenList:
                            coin = (Coin(row,col))
                            coin.rect.x -= self.scrollValue
                            self.allCoins.add(coin)
            self.isCameraMoving = False

    #Control the movement of AI enemy
    def updateFlyManLocation(self):
        for enemies in self.allFlyMan:
            if enemies.lightingGenerated == 5:
                enemies.isDead == True
                enemies.kill()
            if enemies.isDead == False and self.player.isHurt == False:
                enemies.timer += 1
                if enemies.rect.x > self.player.rect.x + 50:
                    enemies.rect.x -= 10
                elif enemies.rect.x < self.player.rect.x - 50:
                    enemies.rect.x += 10
                if enemies.timer == 20:
                    topY = enemies.rect.bottom
                    lighting = (Lighting(enemies.rect.x, topY))
                    self.allSprites.add(lighting)
                    self.allLighting.add(lighting)
                    enemies.timer = 0
                    enemies.lightingGenerated += 1

    #Create a bullet 
    def bulletCreate(self):
        for event in pygame.event.get():
            if (event.type == pygame.MOUSEBUTTONDOWN and self.player.isHurt == False 
            and self.player.bulletNumber > 0):
                (mouseX,mouseY) = pygame.mouse.get_pos()
                (playerX,playerY) = self.player.rect.center
                slopeX = mouseX - playerX
                slopeY = mouseY - playerY
                bullet = Bullet(playerX, playerY, slopeX, slopeY, 15)
                self.allSprites.add(bullet)
                self.allBullets.add(bullet)
                self.player.bulletNumber -= 1
                self.shotSound.play()

    #Update time remained during game
    def playingTimeUpdate(self):
        gameTime = self.clock.get_time()
        self.player.timerGame -= gameTime/1000
        self.timeUsed += gameTime/1000
        if self.player.timerGame <= 0 and (self.mode == game or self.mode == "mazeStart"
        or self.mode == "maze" or self.mode == "mazeSolved"):
            self.mode = "gameOver"

    #Update methods
    def timerFired(self, dt):
        if self.mode == "main":
            self.playSong()
            self.mainKeyPress()
        elif self.mode == "login":
            self.loginKeyPress()
        elif self.mode == "register":
            self.registerKeyPress()
        elif self.mode == "help" or self.mode == "scoreboard":
            self.helpKeyPress()
        elif self.mode == "start":
            self.startKeyPress()
        elif self.mode == "store":
            self.storeKeyPress()
        elif self.mode == "game":
            self.playingTimeUpdate()
            self.playerState()
            self.platformCollision()
            self.boxHitUpdate()
            self.bulletCreate()
            self.coinCollision()
            self.boxCollision()
            self.allCoins.update()
            self.allBoxes.update()
            self.updateFlyManLocation()
            self.allFlyMan.update()
            self.playerGetHurt()
            self.bulletHitEnemies()
            self.allSprites.update()
            self.camera()
            self.backgroundScrolling()
        elif self.mode == "mazeStart":
            self.mazeStartKeyPress()
            self.playingTimeUpdate()
        elif self.mode == "maze":
            self.mazeAi()
            self.makeMove()
            self.allIslands.update()
            self.mazeSolveCheck()
            self.playingTimeUpdate()
        elif self.mode == "mazeSolved":
            self.mazeSolvedKeyPress()
            self.playingTimeUpdate()
        elif self.mode == "gameOver":
            self.gameOverKeyPress()
        elif self.mode == "finish":
            self.gameFinishKeyPress()
            self.gameFinishAddStat()
            self.updateAccountInfo()

    #Redraw screen
    def redrawAll(self):
        if self.mode == "main":
            self.mainScreen()
        elif self.mode == "login":
            self.loginScreen()
        elif self.mode == "register":
            self.registerScreen()
        elif self.mode == "scoreboard":
            self.scoreboardScreen()
            self.compareScore()
        elif self.mode == "help":
            self.helpScreen()
        elif self.mode == "start":
            self.startScreen()
        elif self.mode == "store":
            self.storeScreen()
            self.updateAccountInfo()
        elif self.mode == "game":
            self.screen.blit(self.background,(self.backgroundX,0))
            self.screen.blit(self.background,(self.backgroundX2,0))
            self.tileDrawing()
            self.tileDecor.draw(self.screen)
            self.allCoins.draw(self.screen)
            self.allIcons.draw(self.screen)
            self.allFlyMan.draw(self.screen)
            self.allSprites.draw(self.screen)
            self.allBoxes.draw(self.screen)
            self.drawGameScreen()
        elif self.mode == "mazeStart":
            self.mazeStartScreen()
        elif self.mode == "maze":
            self.screen.fill((255,204,204))
            self.allRods.draw(self.screen)
            self.allIslands.draw(self.screen)
        elif self.mode == "mazeSolved":
            self.mazeSolvedScreen()
        elif self.mode == "gameOver":
            self.gameOverScreen()
        elif self.mode == "finish":
            self.gameFinishScreen()

    #Main game function
    def run(self):
        self.clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.playing = True
        self.isValidMaze()
        while self.playing:
            time = self.clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
            self.redrawAll()
            pygame.display.flip()
        pygame.quit()

    #Control the mode of game based on the state of player
    def playerState(self):
        if self.player.rect.y > 450:
            self.mode = "mazeStart"
            self.mazeSong.play(-1)
        if self.player.health == 0:
            self.mode = "gameOver"
            self.gameOverSound.play()
        if self.player.startJumping == True and self.playerHitItem == False:
            self.jumpSound.play()
            self.player.startJumping = False

    #Main screen UI
    def mainScreen(self):
        startBackground = pygame.transform.scale(
            (pygame.image.load("GUI/greenLandscapeBg.png").convert_alpha()),(850,500))
        self.screen.blit(startBackground,(-10,0))
        self.drawText(self.titleFont,"Candy Run",70,190,90,(0,25,51))

        loginBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnRed.png").convert_alpha()),(170,50))
        self.loginBtnRect = loginBtn.get_rect()
        self.loginBtnRect.x = 315
        self.loginBtnRect.y = 185
        self.screen.blit(loginBtn,(self.loginBtnRect.x,self.loginBtnRect.y))
        self.drawText(self.font,"Login",40,367,190,(255,255,255))

        registerBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnGreen.png").convert_alpha()),(170,50))
        self.registerBtnRect = registerBtn.get_rect()
        self.registerBtnRect.x = 315
        self.registerBtnRect.y = 265
        self.screen.blit(registerBtn,(self.registerBtnRect.x,self.registerBtnRect.y))
        self.drawText(self.font,"Register",40,350,270,(255,255,255))

        scoreboardBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnOrange.png").convert_alpha()),(170,50))
        self.scoreboardBtnRect = scoreboardBtn.get_rect()
        self.scoreboardBtnRect.x = 315
        self.scoreboardBtnRect.y = 345
        self.screen.blit(scoreboardBtn,(self.scoreboardBtnRect.x,self.scoreboardBtnRect.y))
        self.drawText(self.font,"Scoreboard",40,330,350,(255,255,255))

        helpBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnGray.png").convert_alpha()),(170,50))
        self.helpBtnRect = helpBtn.get_rect()
        self.helpBtnRect.x = 315
        self.helpBtnRect.y = 425
        self.screen.blit(helpBtn,(self.helpBtnRect.x,self.helpBtnRect.y))
        self.drawText(self.font,"Help",40,375,430,(255,255,255))

    #Main scren keyboard controls
    def mainKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= self.loginBtnRect.left and mouseX <= self.loginBtnRect.right and mouseY >= self.loginBtnRect.top and mouseY <= self.loginBtnRect.bottom):
                    self.mode = "login"
                    self.clickSound.play()
                elif (mouseX >= self.registerBtnRect.left and mouseX <= self.registerBtnRect.right and mouseY >= self.registerBtnRect.top and mouseY <= self.registerBtnRect.bottom):
                    self.mode = "register"
                    self.clickSound.play()
                elif (mouseX >= self.scoreboardBtnRect.left and mouseX <= self.scoreboardBtnRect.right and mouseY >= self.scoreboardBtnRect.top and mouseY <= self.scoreboardBtnRect.bottom):
                    self.mode = "scoreboard"
                    self.clickSound.play()
                elif (mouseX >= self.helpBtnRect.left and mouseX <= self.helpBtnRect.right and mouseY >= self.helpBtnRect.top and mouseY <= self.helpBtnRect.bottom):
                    self.mode = "help"
                    self.clickSound.play()

    #Login screen UI     
    def loginScreen(self):
        self.screen.fill((229,255,204))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panel.png").convert_alpha()),(700,450))
        self.screen.blit(panel,(50,25))
        self.drawText(self.titleFont,"Login",55,300,80,(9,119,75))
        self.drawText(self.directionFont,"Press return after you entered both username and password",20,170,390,(27,130,94))
        self.drawText(self.directionFont,"Username:",23,255,220,(27,130,94))
        pygame.draw.rect(self.screen, (27,130,94), (355, 220, 160, 25),2)
        self.drawText(self.directionFont,self.userName,20,360,220,(27,130,94))
        self.drawText(self.directionFont,"Password:",23,255,270,(27,130,94))  
        pygame.draw.rect(self.screen, (27,130,94), (355, 270, 160, 25),2)
        self.drawText(self.directionFont,self.password,20,360,270,(27,130,94))
        if self.errorMsg == True:
            self.drawText(self.directionFont,"Wrong login info!",20,320,310,(153,0,0))

    #Login scren keyboard controls
    def loginKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= 355 and mouseX <= 515
                    and mouseY >= 220 and mouseY <= 245):
                    self.enterUserName = True
                    self.enterPassword = False
                    self.clickSound2.play()
                elif (mouseX >= 355 and mouseX <= 515
                    and mouseY >= 270 and mouseY <= 295):
                    self.enterUserName = False
                    self.enterPassword = True
                    self.clickSound2.play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.checkUserInfo():
                    self.errorMsg = False
                    self.mode = "start"
                else:
                    self.errorMsg = True
            elif self.enterUserName == True and event.type == pygame.KEYDOWN:
                keyPressed = pygame.key.name(event.key)
                if keyPressed == "backspace":
                    self.userName = self.userName[:-1]
                elif keyPressed.isalnum() and keyPressed != "space":
                    self.userName += keyPressed
            elif self.enterPassword == True and event.type == pygame.KEYDOWN:
                keyPressed = pygame.key.name(event.key)
                if keyPressed == "backspace":
                    self.password = self.password[:-1]
                elif keyPressed.isalnum() and keyPressed != "space":
                    self.password += keyPressed

    #Check if the account exist/if the username matches the password
    def checkUserInfo(self):
        fileRead = open("userInfo.txt", "r")
        f1 = fileRead.read()
        self.masterDict = {}
        for lines in f1.split("\n"):
            if len(lines) != 0:
                user = []
                for info in lines.split(" "):
                    user.append(info)
            name = user[0]
            self.masterDict[name] = {}
            self.masterDict[name]["password"] = user[1]
            self.masterDict[name]["score"] = user[2]
            self.masterDict[name]["coin"] = user[3]
        fileRead.close()
        if ((self.userName in self.masterDict) and 
        (self.masterDict[self.userName]["password"] == self.password)):
            return True
        else:
            return False

    #Register screen UI
    def registerScreen(self):
        self.screen.fill((229,255,204))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panel.png").convert_alpha()),(700,450))
        self.screen.blit(panel,(50,25))
        self.drawText(self.titleFont,"Register",55,250,80,(9,119,75))
        self.drawText(self.directionFont,"Please only include alphabets and numbers",20,170,390,(27,130,94))
        self.drawText(self.directionFont,"Press return after you created both username and password",20,170,420,(27,130,94))
        self.drawText(self.directionFont,"Username:",23,255,220,(27,130,94))
        pygame.draw.rect(self.screen, (27,130,94), (355, 220, 160, 25),2)
        self.drawText(self.directionFont,self.userName,20,360,220,(27,130,94))
        self.drawText(self.directionFont,"Password:",23,255,270,(27,130,94))  
        pygame.draw.rect(self.screen, (27,130,94), (355, 270, 160, 25),2)
        self.drawText(self.directionFont,self.password,20,360,270,(27,130,94))

    #Register screen keyboard controls
    def registerKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= 355 and mouseX <= 515
                    and mouseY >= 220 and mouseY <= 245):
                    self.enterUserName = True
                    self.enterPassword = False
                    self.clickSound2.play()
                elif (mouseX >= 355 and mouseX <= 515
                    and mouseY >= 270 and mouseY <= 295):
                    self.enterUserName = False
                    self.enterPassword = True
                    self.clickSound2.play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.saveUserInfo()
                self.userName = ""
                self.password = ""
                self.mode = "main"
            elif self.enterUserName == True and event.type == pygame.KEYDOWN:
                keyPressed = pygame.key.name(event.key)
                if keyPressed == "backspace":
                    self.userName = self.userName[:-1]
                elif keyPressed.isalnum() and keyPressed != "space":
                    self.userName += keyPressed
            elif self.enterPassword == True and event.type == pygame.KEYDOWN:
                keyPressed = pygame.key.name(event.key)
                if keyPressed == "backspace":
                    self.password = self.password[:-1]
                elif keyPressed.isalnum() and keyPressed != "space":
                    self.password += keyPressed
    
    #Save a newly registered account info and check if the account already exists
    def saveUserInfo(self):
        fileRead = open("userInfo.txt", "r")
        fileWrite = open("userInfo.txt", "a+")
        #check if the userName exist
        f1 = fileRead.read()
        masterList = set()
        for lines in f1.split("\n"):
            user = []
            for info in lines.split(" "):
                user.append(info)
            name = user[0]
            masterList.add(name)
        if self.userName not in masterList and self.userName != "" and self.password != "":
            fileWrite.write(self.userName + " " + self.password + " " + "0" +  " " + "0" + "\n")
        fileRead.close()
        fileWrite.close()

    #Scoreboard screen UI
    def scoreboardScreen(self):
        self.screen.fill((229,255,204))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panel.png").convert_alpha()),(700,450))
        self.screen.blit(panel,(50,25))
        self.drawText(self.titleFont,"Scoreboard",55,190,80,(9,119,75))
        self.drawText(self.directionFont,"Press any key to return to the main screen",20,215,420,(27,130,94))
    
    # Check the file for top three scores and players
    def compareScore(self):
        f = open("userInfo.txt", "r")
        text = f.read()
        d = {}
        for lines in text.split("\n"):
            if len(lines) != 0:
                user = []
                for info in lines.split(" "):
                    user.append(info)
            name = user[0]
            d[name] = user[2]
        f.close()
        firstPlayer, firstScore = PygameGame.checkHighestScore(d)
        self.drawText(self.directionFont,f"#1   {firstPlayer}: {firstScore}",25,260,190,(27,130,94))
        del d[firstPlayer]
        secondPlayer, secondScore = PygameGame.checkHighestScore(d)
        self.drawText(self.directionFont,f"#2   {secondPlayer}: {secondScore}",25,260,240,(27,130,94))
        del d[secondPlayer]
        thirdPlayer, thirdScore = PygameGame.checkHighestScore(d)
        self.drawText(self.directionFont,f"#3   {thirdPlayer}: {thirdScore}",25,260,290,(27,130,94))
    
    #Helper function that returns the highest score and player in a dictionary
    def checkHighestScore(d):
        highestScore = -1
        highestPlayer = None
        for keys in d:
            if int(d[keys]) > highestScore:
                highestScore = int(d[keys])
                highestPlayer = keys
        return highestPlayer,highestScore

    #Help screen UI
    def helpScreen(self):
        self.screen.fill((229,255,204))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panel.png").convert_alpha()),(700,450))
        self.screen.blit(panel,(50,25))
        self.drawText(self.titleFont,"Direction",55,240,80,(9,119,75))
        self.drawText(self.directionFont,"1) Use arrow keys to control the bunny",23,105,160,(27,130,94))
        self.drawText(self.directionFont,"2) Press mouse to fire a bullet",23,105,210,(27,130,94))
        self.drawText(self.directionFont,"3) Pay attention to the boxes during the adventure for good or",23,105,260,(27,130,94))
        self.drawText(self.directionFont,"bad surprises",23,128,290,(27,130,94))
        self.drawText(self.directionFont,"4) To make the journey more interesting,  jump into the gap",23,105,340,(27,130,94))
        self.drawText(self.directionFont,"without water!!",23,130,370,(27,130,94))
        self.drawText(self.directionFont,"Press any key to return to the main screen",20,215,420,(27,130,94))

    #Login screen keyboard controls
    def helpKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.mode = "main"

    #Start screen UI
    def startScreen(self):
        self.screen.fill((229,255,204))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panel.png").convert_alpha()),(700,450))
        self.screen.blit(panel,(50,25))
        length = len(self.userName) + 3
        center = (length*45)//2
        self.drawText(self.titleFont,f"Hi {self.userName}",45,450-center,80,(9,119,75))

        startBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnRed.png").convert_alpha()),(170,50))
        self.startBtnRect = startBtn.get_rect()
        self.startBtnRect.x = 315
        self.startBtnRect.y = 200
        self.screen.blit(startBtn,(self.startBtnRect.x,self.startBtnRect.y))
        self.drawText(self.font,"Start",40,367,205,(247,242,162))

        storeBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnOrange.png").convert_alpha()),(170,50))
        self.storeBtnRect = storeBtn.get_rect()
        self.storeBtnRect.x = 315
        self.storeBtnRect.y = 300
        self.screen.blit(storeBtn,(self.storeBtnRect.x,self.storeBtnRect.y))
        self.drawText(self.font,"Store",40,367,305,(247,242,162))

    #Start screen keyboard controls
    def startKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= self.startBtnRect.left and mouseX <= self.startBtnRect.right
                    and mouseY >= self.startBtnRect.top and mouseY <= self.startBtnRect.bottom):
                    self.mode = "game"
                    self.menuSong.stop()
                    self.clickSound.play()
                if (mouseX >= self.storeBtnRect.left and mouseX <= self.storeBtnRect.right
                    and mouseY >= self.storeBtnRect.top and mouseY <= self.storeBtnRect.bottom):
                    self.mode = "store"
                    self.clickSound.play()

    #Store screen UI
    def storeScreen(self):
        self.screen.fill((229,255,204))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panel.png").convert_alpha()),(700,450))
        self.screen.blit(panel,(50,25))
        length = len(self.userName) + 3
        center = (length*45)//2
        self.drawText(self.titleFont,f"Hi {self.userName}",45,450-center,80,(9,119,75))
        self.drawText(self.directionFont,f"Coin Count: {self.masterDict[self.userName]['coin']}",20,150,150,(9,119,75))
        self.drawText(self.directionFont,f"Health: {self.player.health}",20,150,180,(9,119,75))
        self.drawText(self.directionFont,f"Bullet: {self.player.bulletNumber}",20,150,210,(9,119,75))
        self.drawText(self.directionFont,"Buy an item by clicking on it, press any key to return to start screen",20,120,430,(9,119,75))
        LivesStore = pygame.transform.scale(
            (pygame.image.load("background/lifes.png").convert_alpha()),(52,71))
        self.LivesStoreRect = LivesStore.get_rect()
        self.LivesStoreRect.x = 250
        self.LivesStoreRect.y = 270
        self.screen.blit(LivesStore,(self.LivesStoreRect.x,self.LivesStoreRect.y))
        self.drawText(self.directionFont,"400",20,266,340,(9,119,75))
        bulletStore = pygame.transform.scale(
            (pygame.image.load("background/carrots.png").convert_alpha()),(54,49))
        self.bulletStoreRect = bulletStore.get_rect()
        self.bulletStoreRect.x = 500
        self.bulletStoreRect.y = 280
        self.screen.blit(bulletStore,(self.bulletStoreRect.x,self.bulletStoreRect.y))
        self.drawText(self.directionFont,"100",20,520,340,(9,119,75))
        if self.purchaseFailed:
            self.drawText(self.directionFont,"Not enough coin!",20,350,400,(153,0,0))

    #Store screen keyboard controls
    #Check if the player has enough money for the item
    def storeKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= self.LivesStoreRect.left and mouseX <= self.LivesStoreRect.right
                    and mouseY >= self.LivesStoreRect.top and mouseY <= self.LivesStoreRect.bottom):
                    coinNum = int(self.masterDict[self.userName]['coin'])
                    coinNum -= 400
                    if coinNum >= 0:
                        self.masterDict[self.userName]['coin'] = str(coinNum)
                        self.player.health += 1
                        self.successPurchase.play()
                        self.purchaseFailed = False
                    else:
                        self.purchaseFailed = True
                        self.failedPurchase.play()
                if (mouseX >= self.bulletStoreRect.left and mouseX <= self.bulletStoreRect.right
                    and mouseY >= self.bulletStoreRect.top and mouseY <= self.bulletStoreRect.bottom):
                    coinNum = int(self.masterDict[self.userName]['coin'])
                    coinNum -= 100
                    if coinNum >= 0:
                        self.masterDict[self.userName]['coin'] = str(coinNum)
                        self.player.bulletNumber += 1
                        self.successPurchase.play()
                        self.purchaseFailed = False
                    else:
                        self.purchaseFailed = True
                        self.failedPurchase.play()
            if event.type == pygame.KEYDOWN:
                self.mode = "start"

    #Update the account info in the file
    #Process of deleting lines adopt from https://intellipaat.com/community/5400/deleting-a-line-from-a-file-in-python
    def updateAccountInfo(self):
        fileRead = open("userInfo.txt", "r")
        f1 = fileRead.read()
        output = []
        for lines in f1.split("\n"):
            if lines.startswith(self.userName):
                output.append(self.userName + " " + self.password + " " + 
                f"{self.masterDict[self.userName]['score']}" +  " " + f"{self.masterDict[self.userName]['coin']}" + "\n")
            else:
                output.append(lines + "\n")
        fileRead.close()
        f = open("userInfo.txt", "w")
        f.writelines(output)
        f.close()      

    #Maze start screen UI
    def mazeStartScreen(self):
        self.screen.fill((204,229,255))
        self.drawText(self.titleFont,"Maze",70,290,90,(0,102,204))
        self.drawText(self.directionFont,"Use arrow keys to help the bunny escape the maze!",30,105,230,(0,76,153))
        self.drawText(self.directionFont,"Your goal is to reach the lower right corner before the enemies!",30,15,300,(0,76,153))
        self.drawText(self.directionFont,"Press any key to start",30,275,370,(0,76,153))

    #Maze start screen keyboard controls
    def mazeStartKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.mode = "maze"

    #Init the values for maze node dictionary
    def makeValue(self,d):
        d["North"] = False
        d["East"] = False
        d["South"] = False
        d["West"] = False
        return d

    #Generate nodes in the maze and construct a dictionary with node numbers as key
    def makeIsland(self):
        x = self.border
        y = self.border
        self.rows = (self.width - (2*self.border))//50
        self.cols = (self.height - (2*self.border))//50
        counter = 0
        for row in range (self.rows+1):
            for col in range (self.cols+1):
                x = row*50+25
                y = col*50+25
                island = Island(counter,col,row,x,y)
                self.allIslands.add(island)
                self.mazeDict[counter] = self.makeValue({})
                counter += 1
    
    #Use random integer function to create random rods that connect nodes together, 
    #update the node dictionary
    def createRandomRod(self):
        for islands in self.allIslands:
            key = islands.counter
            numOne = random.randint(0,3)
            numTwo = random.randint(0,3)
            if (numOne == 0 or numTwo == 0) and islands.row != 0:
                self.mazeDict[islands.counter]["North"] = True
                rod = Rod("North",islands.row,islands.col,islands.x,islands.y)
                self.allRods.add(rod)
            if (numOne == 1 or numTwo == 1) and islands.col != self.rows:
                self.mazeDict[islands.counter]["East"] = True
                rod = Rod("East",islands.row,islands.col,islands.x,islands.y)
                self.allRods.add(rod)
            if (numOne == 2 or numTwo == 2) and islands.row != self.cols:
                self.mazeDict[islands.counter]["South"] = True
                rod = Rod("South",islands.row,islands.col,islands.x,islands.y)
                self.allRods.add(rod)
            if (numOne == 3 or numTwo == 3) and islands.col != 0:
                self.mazeDict[islands.counter]["West"] = True
                rod = Rod("West",islands.row,islands.col,islands.x,islands.y)
                self.allRods.add(rod)

    #Check and update the connection between nodes to make sure that they are mutual
    def checkConnectNeighbor(self):
        for islands in self.allIslands:
            northNeighbor = islands.counter-1
            eastNeighbor = islands.counter+10
            southNeighbor = islands.counter+1
            westNeighbor = islands.counter-10
            if northNeighbor >= 0 and (self.mazeDict[northNeighbor]["South"] == True):
                self.mazeDict[islands.counter]["North"] = True
            if eastNeighbor <= 159 and (self.mazeDict[eastNeighbor]["West"] == True):
                self.mazeDict[islands.counter]["East"] = True
            if southNeighbor <= 159 and (self.mazeDict[southNeighbor]["North"] == True):
                self.mazeDict[islands.counter]["South"] = True
            if westNeighbor >= 0 and (self.mazeDict[westNeighbor]["East"] == True):
                self.mazeDict[islands.counter]["West"] = True

    #Solve the maze through recursive backtracking
    #Adopted from CMU 15-112 Recursion Class Note 
    #https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
    def solveMaze(self,start):
        self.counter += 1
        # base cases
        if start in self.visited:
            return False
        self.visited.append(start)
        if start > 159:
            return False
        if start == 159:
            return True
        if self.counter > 1000:
            return False
        # recursive case
        moves = set()
        if self.mazeDict[start]["North"]:
            moves.add(-1)
        if self.mazeDict[start]["East"]:
            moves.add(10)
        if self.mazeDict[start]["South"]:
            moves.add(1)
        if self.mazeDict[start]["West"]:
            moves.add(-10)
        for move in moves:
            if self.solveMaze(start+move):
                return True
        self.visited.remove(start)
    
    #Check if the maze is valid
    def isValidMaze(self):
        self.makeIsland()
        self.createRandomRod()
        self.checkConnectNeighbor()
        if self.solveMaze(0) != True:
            main()
    
    #Generate a AI maze using the path generated at self.solveMaze()
    def mazeAi(self):
        self.mazeTimer += 1
        if self.mazeTimer == 5:
            if len(self.visited) != 0:
                for islands in self.allIslands:
                    if islands.counter == self.visited[0]:
                        islands.aiOccupied = True
                        if islands.counter == 159:
                            self.mazeSong.stop()
                            self.mode = "gameOver"
                            self.gameOverSound.play()
                self.visited = self.visited[1:]
                self.mazeTimer = 0

    #Control player movement during maze mode 
    def makeMove(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for islands in self.allIslands:
                        if islands.counter == self.currIsland:
                            currIslandSprite = islands

                if event.key == pygame.K_LEFT:
                    for islands in self.allIslands:
                        if ((islands.counter == self.currIsland - 10) and 
                        (self.mazeDict[islands.counter]["East"] == True)):
                            islands.isOccupied = True
                            if islands.counter in self.playerVisted:
                                currIslandSprite.isOccupied = False
                            else:
                                self.playerVisted.add(self.currIsland)
                            self.currIsland = islands.counter
                            break

                elif event.key == pygame.K_RIGHT:
                    for islands in self.allIslands:
                        if ((islands.counter == self.currIsland + 10) and 
                        (self.mazeDict[islands.counter]["West"] == True)):
                            islands.isOccupied = True
                            if islands.counter in self.playerVisted:
                                currIslandSprite.isOccupied = False
                            else:
                                self.playerVisted.add(self.currIsland)
                            self.currIsland = islands.counter
                            break

                elif event.key == pygame.K_UP:
                    for islands in self.allIslands:
                        if ((islands.counter == self.currIsland - 1) and 
                        (self.mazeDict[islands.counter]["South"] == True)):
                            islands.isOccupied = True
                            if islands.counter in self.playerVisted:
                                currIslandSprite.isOccupied = False
                            else:
                                self.playerVisted.add(self.currIsland)
                            self.currIsland = islands.counter
                            break

                elif event.key == pygame.K_DOWN:
                    for islands in self.allIslands:
                        if ((islands.counter == self.currIsland + 1) and 
                        (self.mazeDict[islands.counter]["North"] == True)):
                            islands.isOccupied = True
                            if islands.counter in self.playerVisted:
                                currIslandSprite.isOccupied = False
                            else:
                                self.playerVisted.add(self.currIsland)
                            self.currIsland = islands.counter
                            break          

    #Check if the player solved the maze
    def mazeSolveCheck(self):
        for islands in self.allIslands:
            if islands.counter == 159 and islands.isOccupied == True:
                self.mode = "mazeSolved"
                self.player.score += 2000
    
    #Maze solve screen UI
    def mazeSolvedScreen(self):
        self.screen.fill((204,229,255))
        self.drawText(self.titleFont,"Congrats",70,190,90,(0,102,204))
        self.drawText(self.directionFont,"You solved the maze!",30,285,230,(0,76,153))
        self.drawText(self.directionFont,"Press any key to resume your adventure",30,170,300,(0,76,153))

    #Maze solve keyboard control
    def mazeSolvedKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.mazeSong.stop()
                self.mode = "game"
                self.player.rect.x = 100
                self.player.rect.y = 300

    #Game over UI
    def gameOverScreen(self):
        background = pygame.transform.scale(
            (pygame.image.load("GUI/redLandscapeBg.png").convert_alpha()),(850,500))
        self.screen.blit(background,(-10,0))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panelCloud.png").convert_alpha()),(653,429))
        self.screen.blit(panel,(50,30))
        self.drawText(self.titleFont,"Game Over",50,130,240,(153,0,0))
        cryBunny = pygame.transform.scale(
            (pygame.image.load("player/bunny1_hurt.png").convert_alpha()),(150,174))
        self.screen.blit(cryBunny,(490,220))
        returnBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnGray.png").convert_alpha()),(181,55))
        self.returnBtnRect = returnBtn.get_rect()
        self.returnBtnRect.x = 200
        self.returnBtnRect.y = 325
        self.screen.blit(returnBtn,(self.returnBtnRect.x,self.returnBtnRect.y))
        self.drawText(self.font,"Main Menu",40,220,332,(52,209,167))
    
    #Game over keyboard press
    def gameOverKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= self.returnBtnRect.left and mouseX <= self.returnBtnRect.right
                    and mouseY >= self.returnBtnRect.top and mouseY <= self.returnBtnRect.bottom):
                    self.clickSound.play()
                    main()
    
    #Game finish UI
    def gameFinishScreen(self):
        background = pygame.transform.scale(
            (pygame.image.load("GUI/redLandscapeBg.png").convert_alpha()),(850,500))
        self.screen.blit(background,(-10,0))
        panel = pygame.transform.scale(
            (pygame.image.load("GUI/panelCloud.png").convert_alpha()),(653,429))
        self.screen.blit(panel,(50,30))
        self.drawText(self.titleFont,"You Won",50,130,240,(153,0,0))
        bunny = pygame.transform.scale(
            (pygame.image.load("player/bunny1_stand.png").convert_alpha()),(120,199))
        self.screen.blit(bunny,(530,220))
        returnBtn = pygame.transform.scale(
            (pygame.image.load("GUI/btnRed.png").convert_alpha()),(181,55))
        self.finshReturnBtnRect = returnBtn.get_rect()
        self.finshReturnBtnRect.x = 170
        self.finshReturnBtnRect.y = 325
        self.screen.blit(returnBtn,(self.finshReturnBtnRect.x,self.finshReturnBtnRect.y))
        self.drawText(self.font,"Main Menu",40,190,332,(255,255,204))
        self.drawText(self.directionFont,f"Score: {self.player.score} ",20,405,275,(204,0,0))
        self.drawText(self.directionFont,f"Coin: {self.player.coinCount} ",20,405,305,(204,0,0))
        self.drawText(self.directionFont,f"Time Used: {int(self.timeUsed)} ",20,405,335,(204,0,0))

    #Game finish keyboard controls
    def gameFinishKeyPress(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX,mouseY) = pygame.mouse.get_pos()
                if (mouseX >= self.finshReturnBtnRect.left and mouseX <= self.finshReturnBtnRect.right
                    and mouseY >= self.finshReturnBtnRect.top and mouseY <= self.finshReturnBtnRect.bottom):
                    self.clickSound.play()
                    main()
    
    #Update the user dicionary
    def gameFinishAddStat(self):
        if self.addStat == False:
            coinNum = int(self.masterDict[self.userName]['coin'])
            coinNum += self.player.coinCount
            self.masterDict[self.userName]['coin'] = str(coinNum)
            self.player.score += ((self.player.health)*300 + 
            (self.player.bulletNumber)*100 + int((self.player.timerGame/3)**2))
            if self.player.score > int(self.masterDict[self.userName]["score"]):
                self.masterDict[self.userName]["score"] = str(self.player.score)
            self.addStat = True

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
