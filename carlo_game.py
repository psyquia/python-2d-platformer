import pygame, random
from random import randint
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
win_x = 1280
win_y = 720
win = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Robot Carlo!!!")

#STATES
START, RUNNING, STAGE_2, PAUSED, NEXT_STAGE, GAME_OVER, LOADING = 0,1,2,3,4,5,6
state = START
stage = 1

#Sprites
#walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
#walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

pauseBg = pygame.image.load('MAINFILES/paused.jpg')
char = pygame.image.load('MAINFILES/standing.png')
startWindow = pygame.image.load('MAINFILES/title.jpg')
nxtStageTxt = pygame.image.load('MAINFILES/misc/next_stage.png')
ironArmor = pygame.image.load('MAINFILES/carloIRON/ironCARLO_armor.png')
flyingRight = [pygame.image.load('MAINFILES/carloIRON/fly/r/f%s.png' % frame) for frame in range (1,9)]
flyingLeft = [pygame.image.load('MAINFILES/carloIRON/fly/l/f%s.png' % frame) for frame in range (1,9)]
goblinDeath = [pygame.image.load('other_fx/bubble_exploBIG/g_exp%s.png' % frame) for frame in range(1, 11)]

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('audio/shoot.wav')
golbinDeathS = pygame.mixer.Sound('audio/deathSound.wav')
fireMissile = pygame.mixer.Sound('audio/fireMissile.wav')
mgSound = pygame.mixer.Sound('audio/mgSound.wav')
jumpSound = pygame.mixer.Sound('audio/jumpSound.wav')
hitSound = pygame.mixer.Sound('audio/hit.wav')
music = pygame.mixer.music.load('audio/music.mp3')
#pygame.mixer.music.play(-1)

##--------------------------------------------------------------------------------------------------------##
def collision(l1,r1,t1,b1,l2,r2,t2,b2):
    if(t1 < b2 and b1 > t2):
        if(r1 > l2 and l1 < r2):
            return True

##--------------------------------------------------------------------------------------------------------##
class frameData:
    def __init__(self):
        pass

##--------------------------------------------------------------------------------------------------------##
class player(object):
    def __init__(self, x , y , width, height, maxHealth):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.velY = 0
        self.jumpCd = 0
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
        self.ammo = 0
        self.armor = 'none'
        self.flying = False
        self.flyFrame = 0
        self.fuel = 100
        self.flyEnd = False
        self.maxFuel = 100
        self.fuel = self.maxFuel
        self.flyCd = 0
    def draw(self,win):
        if self.hitFlash <= 0 and self.alive:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if not self.grounded:
                if self.flying:
                    flyAnim = flyingRight if self.right else flyingLeft
                    win.blit(flyAnim[self.flyFrame//3], (self.x,self.y+7))
                    if not self.flyEnd:
                        if self.flyFrame < 23:
                            self.flyFrame+=1
                        else:
                            self.flyFrame = 12
                    else:
                        if self.flyFrame > 8:
                            self.flyFrame = 8
                        win.blit(flyAnim[self.flyFrame//3], (self.x,self.y+7))
                        self.flyFrame-=1
                        if self.flyFrame <= 0:
                            self.flying = False
                            self.flyEnd = False
                else:
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
            #pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            #pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
        else:
            self.hitFlash-=1
        self.hitbox = (self.x+18, self.y+10, 28, 53)
        pygame.draw.rect(win, (255,0,0), (30, 40, 300, 20))
        pygame.draw.rect(win, (0,255,0), (30, 40, (self.health/self.maxHealth) * 300, 20))
        #pygame.draw.rect(win, (0,255,0), self.hitbox, 2) #HITBOX TEST
        pygame.draw.rect(win, (128,128,128), (1080, 645, 100, 15))
        pygame.draw.rect(win, (255,136,0), (1080, 645, (self.fuel/self.maxFuel) * 100, 15))

    def hit(self):
        self.hitFlash = 5
        hitSound.play()
        self.health-=1
        if self.health <= 0:
            self.alive = False

##--------------------------------------------------------------------------------------------------------##
class projectile(object):
    def __init__(self,x,y,radius,color,dir,vel,dmg,xy,fof):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dir = dir
        self.vel = vel * dir
        self.dmg = dmg
        self.xy = xy
        self.fof = fof
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

##--------------------------------------------------------------------------------------------------------##
class pickup(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
    def collision(self):
        global pickups
        if collision(guy.hitbox[0],guy.hitbox[0]+guy.hitbox[2],guy.hitbox[1],guy.hitbox[1]+guy.hitbox[3],
                        self.x-self.radius,self.x+self.radius,self.y+self.radius,self.y-self.radius):
                pickups.pop(pickups.index(self))
                if self.color == (69,255,12):
                    return 'mg'
                elif self.color == (255,69,69):
                    return 'ironArmor'
        #if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]):
        #    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:

##--------------------------------------------------------------------------------------------------------##
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

##--------------------------------------------------------------------------------------------------------##
class enemy(object):
    gobWalkRight = [pygame.image.load('MAINFILES/R%sE.png' % frame) for frame in range(1, 12)]
    gobWalkLeft = [pygame.image.load('MAINFILES/L%sE.png' % frame) for frame in range(1, 12)]
    uShootWalkRight = [pygame.image.load('MAINFILES/enemies/upshooter/r/eR%s.png' % frame) for frame in range(1,5)]
    uShootWalkLeft = [pygame.image.load('MAINFILES/enemies/upshooter/l/eL%s.png' % frame) for frame in range(1,5)]
    def __init__(self,x,y,width,height,end,vel,maxHP,type):
        self.x = x
        self.y = y
        self.width = width
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = vel
        self.hitbox = (self.x + 30, self.y, 28, 60)
        self.maxHealth = maxHP
        self.type = type
        self.health = self.maxHealth
        self.alive = True
        self.hitFlash = 0
        self.deathFrame = 0
    def draw(self,win):
        if self.type == 'goblin':
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
                        win.blit(self.gobWalkRight[self.walkCount//3], (self.x,self.y))
                        self.walkCount += 1
                        self.hitbox = (self.x+15, self.y, 28, 60)
                    else:
                        win.blit(self.gobWalkLeft[self.walkCount//3], (self.x,self.y))
                        self.walkCount += 1
                        self.hitbox = (self.x+30, self.y, 28, 60)
                    #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #  HITBOX TEST
                else:
                    self.hitFlash-=1
                pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
        elif self.type == 'upShooter':
            if not self.alive:
                if self.deathFrame < 30:
                    win.blit(goblinDeath[self.deathFrame//3], (self.x+10,self.y+20))
                    self.deathFrame+=1
                else:
                    goblins.pop(goblins.index(self))
            else:

                if self.hitFlash <= 0:
                    self.move()
                    if self.walkCount + 1 >= 16:
                        self.walkCount = 0
                    if self.vel > 0:
                        win.blit(self.uShootWalkRight[self.walkCount//4], (self.x,self.y))
                        self.walkCount += 1
                        self.hitbox = (self.x+15, self.y, 28, 60)
                    else:
                        win.blit(self.uShootWalkLeft[self.walkCount//4], (self.x,self.y))
                        self.walkCount += 1
                        self.hitbox = (self.x+30, self.y, 28, 60)
                    #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #  HITBOX TEST
                else:
                    self.hitFlash-=1
                pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
    def move(self):
        global bullets, uShootCd
        if self.alive:
            if self.type == 'upShooter':
                if uShootCd <= 0:
                    bullets.append(projectile(round(self.x + self.width-15), self.y-10, 10, (242,0,0), -1, 15,1,'y','foe')) #(249,0,255)
                    uShootCd = 30

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
        global goblins, kills
        self.hitFlash = 4
        hitSound.play()
        self.health-=dmg
        if self.health <= 0:
            golbinDeathS.play()
            kills+=1
            self.alive = False
        #    self.die()
        #    if self.deathFrame > 30: goblins.pop(goblins.index(self))

##--------------------------------------------------------------------------------------------------------##
def redrawGameWindow():
    global stage
    if not stage == 3:
        win.blit(bg, (bgX,0))
        win.blit(bg, (bgX2,0))
        win.blit(bgStatic, (0,bgSplit))
    else:
        win.blit(bg,(0,0))
    text = font.render('Ammo: ' + str(guy.ammo), 1, (230,250,230)) if guy.ammo > 0 else font.render('Ammo: ∞', 1, (230,250,230))
    if not stage == 1:
        fpsCol = (255,255,255)
    else:
        fpsCol = (0,0,0)
    fps = font.render(str(int(clock.get_fps())),1,fpsCol)
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


##--------------------------------------------------------------------------------------------------------##
def drawPausedWindow():
    win.blit(pauseBg, (0,0))
    text = sFont.render('PRESS ESC TO RESUME', 1, (0,150,0))
    text2 = sFont.render("PRESS 'Q' TO QUIT", 2, (200,0,0))
    text3 = sFont.render("CONTROLS",2,(100,100,100))
    text4 = sFont.render("w a s d / arrow keys => move",2,(100,100,100))
    text5 = sFont.render("'space' => shoot",2,(100,100,100))
    win.blit(text, (720, 250))
    win.blit(text2, (720, 300))
    win.blit(text3, (730, 370))
    win.blit(text4, (730, 410))
    win.blit(text5, (730, 450))


##--------------------------------------------------------------------------------------------------------##
def hitUpdate():
    global points,playerHitCd
    for bullet in bullets:
        currPoints = points
        for goblin in goblins:
            if collision(bullet.x-bullet.radius, bullet.x+bullet.radius, bullet.y-bullet.radius, bullet.y+bullet.radius, goblin.hitbox[0],
                            goblin.hitbox[0]+goblin.hitbox[2], goblin.hitbox[1], goblin.hitbox[1]+goblin.hitbox[3]):
                if currPoints == points and bullet.fof == 'friend':
                    if goblin.type == 'upShooter':
                        if bullet.color == (69,255,12):
                            goblin.hit(bullet.dmg)
                            points+=1
                            bullets.pop(bullets.index(bullet))
                    else:
                        goblin.hit(bullet.dmg)
                        points+=1
                        bullets.pop(bullets.index(bullet))
        if collision(bullet.x-bullet.radius, bullet.x+bullet.radius, bullet.y-bullet.radius, bullet.y+bullet.radius, guy.hitbox[0],
                        guy.hitbox[0]+guy.hitbox[2], guy.hitbox[1], guy.hitbox[1]+guy.hitbox[3]):
            if bullet.fof == 'foe':
                guy.hit()
                playerHitCd = 60
                bullets.pop(bullets.index(bullet))
        if (bullet.x < win_x and bullet.x > 0) and (bullet.y < win_y and bullet.y > 0):
            if bullet.xy == 'x':
                bullet.x += bullet.vel
            else:
                bullet.y += bullet.vel
        else:
            if bullet in bullets: bullets.pop(bullets.index(bullet))

    for goblin in goblins:
        if playerHitCd <= 0 and goblin.alive and guy.alive:
            if collision(guy.hitbox[0],guy.hitbox[0]+guy.hitbox[2], guy.hitbox[1], guy.hitbox[1]+guy.hitbox[3],goblin.hitbox[0],
                            goblin.hitbox[0]+goblin.hitbox[2], goblin.hitbox[1], goblin.hitbox[1]+goblin.hitbox[3]):
                guy.hit()
                playerHitCd = 60

##--------------------------------------------------------------------------------------------------------##
def aliveInputs():
    global fireballCd,mgCd,fireMissileCd
    if guy.jumpCd > 0:
        guy.jumpCd-=1
    if not(guy.onPlatform == nonPlatform) and guy.grounded:
        col = guy.onPlatform.collision(guy)
        if not col == 'top':
            guy.grounded = False
    if guy.grounded:
        guy.flying = False
        if keys[pygame.K_UP] or keys[pygame.K_w] and guy.jumpCd == 0:
            jumpSound.play()
            guy.velY = -12
            guy.grounded = False
            guy.jumpCd = 20
    else:
        if guy.armor == 'ironCarlo':
            if guy.velY > 0 and (keys[pygame.K_UP] or keys[pygame.K_w]):
                guy.flying = True
                guy.flyFrame = 0
                guy.flyAnimCd = 10
            if (keys[pygame.K_UP] or keys[pygame.K_w]):
                if guy.flying:
                    if guy.fuel > 0 and guy.flyCd == 0:
                        guy.velY = -4.5
                    else:
                        if guy.flyCd == 0:
                            guy.flyCd = 20
                        else:
                            guy.flyCd -=1
            elif guy.flying:
                guy.flyEnd = True
        colflag = False
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
                guy.flying = False
                guy.jumpFrame = 0
                guy.onPlatform = currPlatform
                walkLockR,walkLockL = False,False
            else:
                walkLockR,walkLockL = False,False
        if not guy.grounded:
            guy.velY += guy.acc
            guy.y += guy.velY + 0.5 * guy.acc
    if col == 'fromLeft' or col == 'fromRight':
        if walkLockR:
            if guy.hitbox[0] + guy.hitbox[2] < guy.onPlatform.x+15: walkLockR = False
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
                bullets.append(projectile(round(guy.x + guy.width // 2), round(guy.y + guy.height //2), 10, (242,0,0), dir, 15,1,'x','friend'))
        elif guy.gun == 'mg':
            if mgCd <= 0:
                mgSound.play()
                mgCd = 8
                if guy.left:
                    dir = -1
                else:
                    dir = 1
                guy.ammo-=1
                bullets.append(projectile(round(guy.x+guy.width//2) + 5 * dir, round(guy.y+guy.height//2), 6, (69,255,12), dir, 17, 0.35,'x','friend'))
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

##--------------------------------------------------------------------------------------------------------##
def pickupUpdate(currP):
    global state
    colType = currP.collision()
    if  colType == 'mg':
        guy.gun = 'mg'
        guy.ammo = 100
    elif colType == 'ironArmor':
        state = NEXT_STAGE
##--------------------------------------------------------------------------------------------------------##
def run_loop():
    global fireballCd,playerHitCd,fireMissileCd,uShootCd,flag,keyHeld,walkLockR, walkLockL, bgX, bgX2, mgCd,state,keys
    hitUpdate()
    if len(goblins) == 1 and kills < killGoal-1:
    	ran = random.randint(0,9999)
    	if ran%2==0:
    		goblins.append(enemy(0-30, 508, 60, 60, 1280-30,4,2,'goblin'))
    	else:
        	goblins.append(enemy(1280-30, 508, 60, 60, 0-30,-4,2,'goblin'))
    for currPickup in pickups:
        pickupUpdate(currPickup)
    keys = pygame.key.get_pressed()
    if not keys[pygame.K_ESCAPE]:
        keyHeld = False
    if guy.alive:
        aliveInputs()
    else:
        state = GAME_OVER
    if not keyHeld and keys[pygame.K_ESCAPE]:
        state = PAUSED
        keyHeld = True
    if guy.velY < 0 and guy.flying and guy.fuel >= 0:
        guy.fuel -=1
    elif guy.fuel < guy.maxFuel+1.7:
        guy.fuel +=1.7
    if fireballCd >= 0: fireballCd-=1
    if mgCd >= 0: mgCd-=1
    if playerHitCd >= 0: playerHitCd-=1
    if uShootCd >= 0: uShootCd-=1
    if not guy.gun =='fireball' and guy.ammo <= 0:
        guy.gun = 'fireball'
        fireballCd = 50
    bgX-=0.3
    bgX2-=0.3
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    redrawGameWindow()

##--------------------------------------------------------------------------------------------------------##
def startStage_1():
    global guy,goblins,platforms,pickups,bg,bgStatic,bgSplit, killGoal, state,walkRight,walkLeft,jumpLeft,jumpRight, points
    points = 0
    state = RUNNING
    bgSplit = 485
    walkRight = [pygame.image.load('MAINFILES/carloB/walkR/R%s.png' % frame) for frame in range(1, 10)]
    walkLeft = [pygame.image.load('MAINFILES/carloB/walkL/L%s.png' % frame) for frame in range(1, 10)]
    jumpLeft = [pygame.image.load('MAINFILES/jumpL/J%sL.png' % frame) for frame in range(1,4)]
    jumpRight = [pygame.image.load('MAINFILES/jumpR/J%sR.png' % frame) for frame in range(1,4)]
    bg = pygame.image.load('bg/cloudlvlLighter.jpg')
    bgStatic = pygame.image.load('bg/cloudlvlStatic.jpg')
    guy = player(100, 200, 64, 64,3) #503.85
    goblins = [enemy(150, 508, 60, 60, 500,4,2,'goblin'),enemy(1250, 508, 60, 60, 510,-4,2,'goblin')]
    platforms = [platform(0,560,1280,150,(200,200,200)), platform(550,475,150,20,(255,255,255)),platform(350,405,150,20,(255,255,255)),platform(750,405,150,20,(255,255,255))]
    pickups = [pickup(825,392,8,(69,255,12))]
    killGoal = 5

def startStage_2():
    global state,guy,goblins,platforms,pickups,bg,bgStatic,bgSplit,walkRight,walkLeft,jumpLeft,jumpRight, killGoal
    bgSplit = 312
    bg = pygame.image.load('bg/nightlvlTOP.jpg')
    bgStatic = pygame.image.load('bg/nightlvlBOT.jpg')
    walkRight.clear()
    walkLeft.clear()
    jumpLeft.clear()
    jumpRight.clear()
    walkRight = [pygame.image.load('MAINFILES/carloDia/walkR/R%s.png' % frame) for frame in range(1,10)]
    walkLeft = [pygame.image.load('MAINFILES/carloDia/walkL/L%s.png' % frame) for frame in range(1,10)]
    jumpLeft = [pygame.image.load('MAINFILES/carloDia/jump/J%sL.png' % frame) for frame in range(1,4)]
    jumpRight = [pygame.image.load('MAINFILES/carloDia/jump/J%sR.png' % frame) for frame in range(1,4)]
    state = RUNNING
    guy = player(100, 200, 64, 64,3) #503.85
    goblins = [enemy(150, 508, 60, 60, 500,4,2,'goblin'),enemy(1250, 480, 60, 60, 510,-4,5,'upShooter')]
    platforms = [platform(0,560,1280,150,(200,200,200)), platform(900,200,150,20,(255,255,255)),platform(680,250,100,20,(255,255,255)),platform(530,320,50,20,(255,255,255)),platform(440,400,50,20,(255,255,255)),platform(350,480,50,20,(255,255,255))]
    pickups = [pickup(975,187,8,(69,255,12))]
    killGoal = 5

def startStage_3():
    global state,guy,goblins,platforms,pickups,bg,bgStatic,bgSplit,walkRight,walkLeft,jumpLeft,jumpRight, killGoal
    walkRight.clear()
    walkLeft.clear()
    jumpLeft.clear()
    jumpRight.clear()
    walkRight = [pygame.image.load('MAINFILES/carloIRON/walk/R/R%s.png' % frame) for frame in range(1, 10)]
    walkLeft = [pygame.image.load('MAINFILES/carloIRON/walk/L/L%s.png' % frame) for frame in range(1, 10)]
    jumpLeft = [pygame.image.load('MAINFILES/carloIRON/jump/L/J%sL.png' % frame) for frame in range(1,4)]
    jumpRight = [pygame.image.load('MAINFILES/carloIRON/jump/R/J%sR.png' % frame) for frame in range(1,4)]
    bg = pygame.image.load('bg/nabooHmm.jpg')
    bgStatic = pygame.image.load('bg/cloudlvlStatic.jpg')
    state = RUNNING
    bgSplit = 485
    guy = player(100, 200, 64, 64,3) #503.85
    guy.armor = 'ironCarlo'
    goblins = [enemy(150, 508, 60, 60, 500,4,2,'goblin'),enemy(1250, 508, 60, 60, 510,-4,2,'goblin')]
    platforms = [platform(0,560,1280,150,(99,48,0)), platform(770,215,200,20,(99,48,0))]
    pickups = [pickup(825,207,8,(69,255,12))]
    killGoal = 5

##--------------------------------------------------------------------------------------------------------##
def startGame():
    global points,bullets,fireballCd,playerHitCd,fireMissileCd,uShootCd,keyHeld,walkLockR, walkLockL, nonPlatform, bgX, bgX2, mgCd,font,pFont,sFont, kills, textFlash
    bgX = 0
    bgX2 = bg.get_width()
    points = 0
    bullets = []
    nonPlatform = platform(0,0,0,0,(0,0,0))
    kills = 0
    fireballCd = 30
    mgCd = 5
    playerHitCd, fireMissileCd, uShootCd, textFlash = 0,0,0,0
    keyHeld, walkLockR, walkLockL= False, False, False

##--------------------------------------------------------------------------------------------------------##
#mainLoop
# text

def main():
    global state, stage, font, kills, textFlash, sFont, keyHeld
    flag = True
    font = pygame.font.SysFont('comicsansms', 25,2)
    pFont = pygame.font.SysFont("timesnewroman", 30,2)
    sFont = pygame.font.SysFont("impact", 35)
    sFont1 = pygame.font.SysFont("impact", 25)
    while flag:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        if state == LOADING:
            if stage == 1: startStage_1()
            elif stage == 2: startStage_2()
            elif stage == 3: startStage_3()
            startGame()
            state = RUNNING
        elif state == RUNNING:
            if stage == 1:
                run_loop()
                if kills == killGoal:
                    state = NEXT_STAGE
            elif stage == 2:
                run_loop()
                if kills == killGoal:
                    pickups.append(pickup(975,187,8,(255,69,69)))
                    kills+=1
                elif kills > killGoal:
                    win.blit(ironArmor,(945,137))
            elif stage == 3:
                run_loop()
                if kills == killGoal:
                    state = NEXT_STAGE
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
                state = LOADING
        elif state == GAME_OVER:
            pygame.draw.rect(win, (0,0,0), (0, 0, 1280, 720))
            text1 = sFont.render("You Died.", 4, (255,255,255))
            text2 = sFont.render("Press 'SPACE' to restart.", 4, (255,255,255))
            win.blit(text1, (430,300))
            win.blit(text2, (400,500))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                state = LOADING
        elif state == NEXT_STAGE:
            pygame.draw.rect(win, (0,0,0), (0, 0, 1280, 720))
            text = sFont1.render("press ENTER to continue. . .", 0,(255,255,255))
            win.blit(text,(450,450))
            if textFlash<37:
                textFlash +=1
                if textFlash < 20:
                    win.blit(nxtStageTxt,(400,250))
            else:
                textFlash = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
            	state = LOADING
            	if stage == 3:
            		stage = 1
            	else:
                	stage+=1;
        clock.tick(63)

    pygame.quit()

if __name__ == "__main__":
    main()
