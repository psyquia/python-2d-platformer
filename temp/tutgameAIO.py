import pygame, random
from random import randint
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
win_x = 1280
win_y = 720
win = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Robot Carlo!!!")

if False:
    import pygame._view
#STATES
START, RUNNING, PAUSED, NEXT_LEVEL, GAME_OVER = 0,1,2,3,4
state = START
#Sprites
print("importing files")

walkRight = [pygame.image.load('R%s.png' % frame) for frame in range(1, 10)]
#walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L%s.png' % frame) for frame in range(1, 10)]
#walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('cloudlvlLighter.jpg')
bgStatic = pygame.image.load('cloudlvlStatic.jpg')
pauseBg = pygame.image.load('newpauseplain.jpg')
gameOverBg = pygame.image.load('aha.jpg')
char = pygame.image.load('standing.png')
startWindow = pygame.image.load('newpausetitle.jpg')
jumpLeft = [pygame.image.load('J%sL.png' % frame) for frame in range(1,4)]
jumpRight = [pygame.image.load('J%sR.png' % frame) for frame in range(1,4)]
flying = [pygame.image.load('MAINFILES/carloIRON/fly/f%s.png' % frame) for frame in range (1,9)]
goblinDeath = [pygame.image.load('g_exp%s.png' % frame) for frame in range(1, 11)]

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('shoot.wav')
golbinDeathS = pygame.mixer.Sound('deathSound.wav')
fireMissile = pygame.mixer.Sound('fireMissile.wav')
mgSound = pygame.mixer.Sound('mgSound.wav')
jumpSound = pygame.mixer.Sound('jumpSound.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play(-1)

#Player
print("done importing files")

class player(object):
    def __init__(self, x , y , width, height, maxHealth):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.velY = 0
        self.isJump = False
        self.jumpCount = 0
        self.left = False
        self.right = True
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x+18, self.y+10, 28, 53)
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.alive = True
        self.hitFlash = 0
        self.jumpFrame = 0
        self.falling = False
        self.grounded = False
        self.acc = 0.7
        self.onPlatform = platform(0,0,0,0,(0,0,0))
        self.gun = 'fireball'
        self.flying = False
    def draw(self,win):
        if self.hitFlash <= 0 and self.alive:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if not self.grounded:
                if self.left:
                    if self.jumpFrame < 9:
                        win.blit(jumpLeft[self.jumpFrame//3], (self.x,self.y))
                        self.jumpFrame += 1
                    else:
                        win.blit(jumpLeft[2], (self.x,self.y))
                if self.right:
                    if self.jumpFrame < 9:
                        win.blit(jumpRight[self.jumpFrame//3], (self.x,self.y))
                        self.jumpFrame += 1
                    else:
                        win.blit(jumpRight[2], (self.x,self.y))
            else:
                if not(self.standing):
                    if self.left:
                        win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                        self.walkCount += 1
                    elif self.right:
                        win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                        self.walkCount += 1
                else:
                    if self.right:
                        win.blit(walkRight[0], (self.x,self.y))
                    else:
                        win.blit(walkLeft[0], (self.x,self.y))
            #pygame.draw.rect(win, (0,255,0), self.hitbox, 2) #HITBOX TEST
            #pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            #pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
        else:
            self.hitFlash-=1
        self.hitbox = (self.x+18, self.y+10, 28, 53)
        pygame.draw.rect(win, (255,0,0), (30, 40, 300, 20))
        pygame.draw.rect(win, (0,255,0), (30, 40, (self.health/self.maxHealth) * 300, 20))
    #    pygame.draw.rect(win, (0,255,0), self.hitbox, 2) #HITBOX TEST

    def hit(self):
        self.hitFlash = 5
        hitSound.play()
        self.health-=1
        if self.health <= 0:
            self.alive = False
print("done with player")

class projectile(object):
    def __init__(self,x,y,radius,color,dir,vel,dmg):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dir = dir
        self.vel = vel * dir
        self.dmg = dmg
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
print("done with projectile")

class pickup(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
    def collision(self):
        if guy.hitbox[0] + guy.hitbox[2] > self.x-self.radius and guy.hitbox[0] < self.x+self.radius:
            if guy.hitbox[1] + guy.hitbox[3] > self.y+self.radius and guy.hitbox[1] < self.y:
                guy.gun = 'mg'
                pickups.pop(pickups.index(self))
        #if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]):
        #    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
print("done with pickup")

class platform(object):
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height))
    def collision(self,player):

        if player.hitbox[0] + player.hitbox[2] > self.x-6 and player.hitbox[0] + player.hitbox[2] < self.x+6:
            if player.hitbox[1] + player.hitbox[3] > self.y and player.hitbox[1] < self.y + self.height:
                player.x = self.x-49
                return 'fromLeft'
        if player.hitbox[0] > self.x + self.width-6 and player.hitbox[0] < self.x+self.width+6:
            if player.hitbox[1] + player.hitbox[3] > self.y and player.hitbox[1] < self.y + self.height:
                player.x = self.x + self.width-17
                return 'fromRight'

        if player.hitbox[0] + player.hitbox[2] > self.x and player.hitbox[0] < self.x + self.width:
            if player.hitbox[1] > self.y + self.height-9 and player.hitbox[1] < self.y + self.height:
                player.velY = 0
                return 'bottom'
        if player.hitbox[0] + player.hitbox[2] > self.x and player.hitbox[0] < self.x + self.width-10:
            if player.velY < 0:
                return 'none'
            elif player.hitbox[1] + player.hitbox[3] > self.y-9 and player.hitbox[1] + player.hitbox[3] < self.y+20:
                player.y = self.y-60
                return 'top'
        else:
            if player.hitbox[0] + player.hitbox[2] > self.x-10 and player.hitbox[0] < self.x + self.width-10:
                if player.hitbox[1] + player.hitbox[3] > self.y-7 and player.hitbox[1] + player.hitbox[3] < self.y+7:
                    return 'onPlatform'
        return 'none'
print("done with platform")

def redrawGameWindow():
    win.blit(bg, (bgX,0))
    win.blit(bg, (bgX2,0))
    win.blit(bgStatic, (0,485))
    text = font.render('::: ' + str(points), 1, (230,250,230))
    fps = font.render(str(int(clock.get_fps())),1,(0,0,0))
    win.blit(text, (1100, 10))
    win.blit(fps, (15, 10))

    for currPickup in pickups:
        currPickup.draw(win)

    guy.draw(win)
    for currPlatform in platforms[1:]:
        currPlatform.draw(win)
    for goblin in goblins:
        #if goblin.alive:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()
print("done with gamewindow")

def drawPausedWindow():
    win.blit(pauseBg, (0,0))
    text = sFont.render('PRESS ESC TO RESUME', 1, (0,150,0))
    text2 = sFont.render("PRESS 'Q' TO QUIT", 2, (200,0,0))
    win.blit(text, (720, 250))
    win.blit(text2, (720, 300))
print("done with pauseWindow")

def startGame():
    global points,guy,goblins,bullets,fireballCd,playerHitCd,fireMissileCd,flag,keyHeld,platforms,walkLockR, walkLockL, nonPlatform, bgX, bgX2, pickups, mgCd, font, pFont, sFont
    print("done with globals")
    font = pygame.font.SysFont("comicsansms", 30)
    print("done with fonts1")
    pFont = pygame.font.SysFont("timesnewroman", 30)
    print("done with fonts2")
    sFont = pygame.font.SysFont("impact", 35)
    print("done with fonts3")
    bgX = 0
    bgX2 = bg.get_width()
    print("done with bgX")

    points = 0
    guy = player(100, 200, 64, 64,3) #503.85
    #goblin = enemy(100, 513, 60, 60, 450)
    goblins = [enemy(150, 508, 60, 60, 500,4,2),enemy(1250, 508, 60, 60, 510,-4,2)]
    bullets = []
    nonPlatform = platform(0,0,0,0,(0,0,0))
    platforms = [platform(0,560,1280,150,(200,200,200)), platform(550,475,150,20,(255,255,255)),platform(350,405,150,20,(255,255,255)),platform(750,405,150,20,(255,255,255))]
    pickups = [pickup(825,392,8,(69,255,12))]
    fireballCd = 30
    mgCd = 5
    playerHitCd = 0
    fireMissileCd = 0
    flag, keyHeld, walkLockR, walkLockL = True, True, False, False
    print("done with bgX")


print("done with startgame")


class enemy(object):
    walkRight = [pygame.image.load('R%sE.png' % frame) for frame in range(1, 12)]
    walkLeft = [pygame.image.load('L%sE.png' % frame) for frame in range(1, 12)]
    def __init__(self,x,y,width,height,end,vel,maxHP):
        self.x = x
        self.y = y
        self.width = width
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = vel
        self.hitbox = (self.x + 30, self.y, 28, 60)
        self.maxHealth = maxHP
        self.health = self.maxHealth
        self.alive = True
        self.hitFlash = 0
        self.deathFrame = 0
    def draw(self,win):
        if not self.alive:
            if self.deathFrame < 30:
                win.blit(goblinDeath[self.deathFrame//3], (self.x,self.y))
                self.deathFrame+=1
            else:
                goblins.pop(goblins.index(self))
        else:

            if self.hitFlash <= 0:
                if self.walkCount < 21: self.move()
                if self.walkCount + 1 >= 33:
                    self.walkCount = 0
                if self.vel > 0:
                    win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                    self.hitbox = (self.x+15, self.y, 28, 60)
                else:
                    win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                    self.hitbox = (self.x+30, self.y, 28, 60)
                #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #  HITBOX TEST
            else:
                self.hitFlash-=1
            #pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            #pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
    def move(self):
        if self.alive:
            if self.vel > 0:
                endP = self.path[0] if self.path[0] > self.path[1] else self.path[1]
                if self.x + self.vel < endP:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                startP = self.path[1] if self.path[1] < self.path[0] else self.path[0]
                if self.x - self.vel > startP:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.x+=10
                    self.walkCount = 0
    def die(self):
        if self.deathFrame <= 30:
            win.blit(goblinDeath[self.deathFrame//3], (self.x,self.y))
            self.deathFrame+=1

    def hit(self, dmg):
        global goblins
        self.hitFlash = 4
        hitSound.play()
        self.health-=dmg
        if self.health <= 0:
            golbinDeathS.play()
            self.alive = False
        #    self.die()
        #    if self.deathFrame > 30: goblins.pop(goblins.index(self))
print("done with enemy")

#mainLoop
# text

print("about to startgame()")
startGame()
while flag:
    print("in mainloop")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
    #    if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_p: state = PAUSED
        #    if event.key == pygame.K_SPACE:
        #        if state != RUNNING:
            #        state = RUNNING

    if state == RUNNING:
        for bullet in bullets:
            currPoints = points
            for goblin in goblins:
                if goblin.alive and (bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]):
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                        if currPoints == points:
                            goblin.hit(bullet.dmg)
                            points+=1
                            bullets.pop(bullets.index(bullet))
            if bullet.x < win_x and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        for goblin in goblins:
            if playerHitCd <= 0 and goblin.alive and guy.alive and (guy.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and guy.hitbox[1] + guy.hitbox[3] > goblin.hitbox[1]):
                if guy.hitbox[0] + guy.hitbox[2] > goblin.hitbox[0] and guy.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    guy.hit()
                    playerHitCd = 60
        if not goblins:
            #goblins.append(enemy(randint(50,400), 513, 60, 60, randint(410,1200)))
            goblins.append(enemy(0-30, 508, 60, 60, 1280-30,4,2))
            goblins.append(enemy(1280-30, 508, 60, 60, 0-30,-4,2))
        for currPickup in pickups:
            currPickup.collision()
            currPickup.draw(win)


        keys = pygame.key.get_pressed()
        if not keys[pygame.K_ESCAPE]:
            keyHeld = False
        if guy.alive:
            if guy.jumpCount > 0:
                guy.jumpCount-=1

            if not(guy.onPlatform == nonPlatform) and guy.grounded:
                col = guy.onPlatform.collision(guy)
                if not col == 'top':
                    guy.grounded = False
            if guy.grounded:
                if keys[pygame.K_UP] or keys[pygame.K_w] and guy.jumpCount == 0:
                    jumpSound.play()
                    guy.velY = -12
                    #guy.walkCount = 0
                    guy.grounded = False
                    guy.jumpCount = 20
            else:

                colFlag = False
                for currPlatform in platforms:
                    col = currPlatform.collision(guy)
                    if col == 'fromLeft':
                        walkLockR = True
                        guy.onPlatform = currPlatform
                    elif col == 'fromRight':
                        walkLockL = True
                        guy.onPlatform = currPlatform
                    elif col == 'top':
                        guy.grounded = True
                        guy.jumpFrame = 0
                        guy.onPlatform = currPlatform
                        walkLockR,walkLockL = False,False
                    else:
                        walkLockR,walkLockL = False,False


                    #player.x = self.x-45
                if not guy.grounded:
                    guy.velY += guy.acc
                    guy.y += guy.velY + 0.5 * guy.acc
            if col == 'fromLeft' or col == 'fromRight':
                if walkLockR:
                    if guy.hitbox[0] + guy.hitbox[2] < guy.onPlatform.x+15: walkLockR = False
                    #if player.hitbox[0] + player.hitbox[2] > self.x+15 and player.hitbox[0] < self.x + self.width-10:
                if walkLockL:
                    if guy.hitbox[0] > guy.onPlatform.x + guy.onPlatform.width + 15: #walkLockL = False
                        walkLockL = False
            else:
                walkLockR = False
                walkLockL = False

            if keys[pygame.K_SPACE]:
                if guy.gun == 'fireball':
                    if fireballCd <= 0:
                        if fireMissileCd <= 0:
                            fireMissile.play()
                            fireMissileCd = 2
                        else:
                            fireMissileCd-=1
                        bulletSound.play()
                        fireballCd = 50
                        if guy.left:
                            dir = -1
                        else:
                            dir = 1
                        bullets.append(projectile(round(guy.x + guy.width // 2), round(guy.y + guy.height //2), 10, (255,0,0), dir, 15,1))
                elif guy.gun == 'mg':
                    if mgCd <= 0:
                        mgSound.play()
                        mgCd = 8
                        if guy.left:
                            dir = -1
                        else:
                            dir = 1
                        bullets.append(projectile(round(guy.x+guy.width//2) + 5 * dir, round(guy.y+guy.height//2), 6, (69,255,12), dir, 17, 1))
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and guy.x > -20 and not walkLockL:
                guy.x-=guy.vel
                guy.left = True
                guy.right = False
                guy.standing = False
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and guy.x < win_x-40 and not walkLockR:
                guy.x+=guy.vel
                guy.right = True
                guy.left = False
                guy.standing = False
            else:
                guy.standing = True
                guy.walkCount = 0

        else:
            state = GAME_OVER
        if not keyHeld and keys[pygame.K_ESCAPE]:
            state = PAUSED
            keyHeld = True

        #    else:
        if fireballCd >= 0: fireballCd-=1
        if mgCd >= 0: mgCd-=1
        if playerHitCd >= 0: playerHitCd-=1

        bgX-=0.3
        bgX2-=0.3
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        redrawGameWindow()
    elif state == PAUSED:
        drawPausedWindow()
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_ESCAPE]:
            keyHeld = False
        if not keyHeld and keys[pygame.K_ESCAPE]:
            state = RUNNING
            keyHeld = True
        if keys[pygame.K_q]:
            flag = False
        if keys[pygame.K_r]:
            state = GAME_OVER
    elif state == START:
        win.blit(startWindow, (0,0))
        text = sFont.render("Press 'SPACE' to start!",4, (0,200,255))
        win.blit(text,(750,550))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            state = RUNNING
            startGame()
    elif state == GAME_OVER:
        pygame.draw.rect(win, (0,0,0), (0, 0, 1280, 720))
        #win.blit(gameOverBg, (200,200))
        text1 = sFont.render("You Died.", 4, (255,255,255))
        text2 = sFont.render("Press 'SPACE' to restart.", 4, (255,255,255))
        win.blit(text1, (430,300))
        win.blit(text2, (400,500))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            state = RUNNING
            startGame()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

"""if not(guy.isJump):
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        jumpSound.play()
        guy.isJump = True
        guy.walkCount = 0
else:

    if guy.jumpCount >= -13:
        col = box.collision(guy)
        print(guy.isJump)
        print(guy.jumpCount)
        #print(col)
        print('box y is ', box.y)
        print('player y is ',guy.hitbox[1] + guy.hitbox[3])

        if col == 'top':
            guy.isJump = False
            guy.jumpCount = 13
            guy.jumpFrame = 0
            guy.grounded = True
        elif col == 'side':
            guy.isJump = False
        elif col == 'bottom':
            guy.isJump = False
        else:
            guy.y -= (guy.jumpCount * abs(guy.jumpCount)) * 0.1
            guy.jumpCount -= 1
            guy.grounded = False

        #if jumpCount == -9.5:
            #jumpCount = -10.1
    else:
        guy.jumpCount = 13
        guy.isJump = False
        guy.jumpFrame = 0
        guy.grounded = True"""
