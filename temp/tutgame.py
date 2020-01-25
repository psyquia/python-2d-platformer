import pygame
pygame.init()
win_x = 1280
win_y = 720
win = pygame.display.set_mode((1280,720))
pygame.display.set_caption("way wha")

#Sprites
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('audio/shoot.wav')
fireMissile = pygame.mixer.Sound('audio/fireMissile.wav')
hitSound = pygame.mixer.Sound('audio/hit.wav')
music = pygame.mixer.music.load('audio/music.mp3')
pygame.mixer.music.play(-1)

#Player
class player(object):
    def __init__(self, x , y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 13
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x+18, self.y+10, 28, 53)
        self.maxHealth = 3
        self.health = self.maxHealth
        self.alive = True
        self.hitFlash = 0
    def draw(self,win):
        if self.hitFlash <= 0:
            if self.alive:
                if self.walkCount + 1 >= 27:
                    self.walkCount = 0

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
                self.hitbox = (self.x+18, self.y+10, 28, 53)
                pygame.draw.rect(win, (0,255,0), self.hitbox, 2) #HITBOX TEST
                pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
        else:
            self.hitFlash-=1
    def hit(self):
        self.hitFlash = 5
        hitSound.play()
        self.health-=1
        print('playerhit')
        if self.health <= 0:
            self.alive = False
class projectile(object):
    def __init__(self,x,y,radius,color,dir,vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dir = dir
        self.vel = vel * dir
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('::: ' + str(points), 1, (230,250,230))
    fps = font.render(str(int(clock.get_fps())),1,(0,0,0))
    win.blit(text, (1100, 10))
    win.blit(fps, (100, 10))
    if goblin.alive: goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    guy.draw(win)
    pygame.display.update()

class enemy(object):
    walkRight = [pygame.image.load('R%sE.png' % frame) for frame in range(1, 12)]
    walkLeft = [pygame.image.load('L%sE.png' % frame) for frame in range(1, 12)]
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 30, self.y, 28, 60)
        self.maxHealth = 5
        self.health = self.maxHealth
        self.alive = True
        self.hitFlash = 0
    def draw(self,win):
        if self.hitFlash <= 0:
            self.move()
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
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #  HITBOX TEST
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, (self.health/self.maxHealth) * 50, 10))
        else:
            self.hitFlash-=1
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x+=10
                self.walkCount = 0
    def hit(self):
        hitFlash = 5
        hitSound.play()
        self.health-=1
        print('hit')
        if self.health <= 0:
            self.alive = False

#mainLoop
# text
points = 0
font = pygame.font.SysFont('comicsans', 30, True, True)

guy = player(50, 508, 64, 64)
goblin = enemy(100, 513, 60, 60, 450)
bullets = []
bulletsCd = 0
playerHitCd = 0
fireMissileCd = 0
charged = 0
flag = True
while flag:
    clock.tick(62)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    for bullet in bullets:
        if goblin.alive and (bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]):
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                points+=1
                bullets.pop(bullets.index(bullet))
        if bullet.x < win_x and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if playerHitCd <= 0 and goblin.alive and guy.alive and (guy.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and guy.hitbox[1] + guy.hitbox[3] > goblin.hitbox[1]):
        if guy.hitbox[0] + guy.hitbox[2] > goblin.hitbox[0] and guy.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            guy.hit()
            playerHitCd = 60

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        flag = False
    if keys[pygame.K_SPACE]:
        if bulletsCd <= 0:
            if fireMissileCd <= 0:
                fireMissile.play()
                fireMissileCd = 2
            else:
                fireMissileCd-=1
            bulletSound.play()
            bulletsCd = 50
            if guy.left:
                dir = -1
            else:
                dir = 1
            bullets.append(projectile(round(guy.x + guy.width // 2), round(guy.y + guy.height //2), 10, (255,0,0), dir, 15))
    #    else:
    bulletsCd-=1
    playerHitCd-=1
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and guy.x > -20 :
        guy.x-=guy.vel
        guy.left = True
        guy.right = False
        guy.standing = False
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and guy.x < win_x-40:
        guy.x+=guy.vel
        guy.right = True
        guy.left = False
        guy.standing = False
    else:
        guy.standing = True
        guy.walkCount = 0
    if not(guy.isJump):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            guy.isJump = True
            guy.walkCount = 0
    else:
        if guy.jumpCount >= -13:
            guy.y -= (guy.jumpCount * abs(guy.jumpCount)) * 0.1
            guy.jumpCount -= 1
            #if jumpCount == -9.5:
                #jumpCount = -10.1
        else:
            guy.jumpCount = 13
            guy.isJump = False
    redrawGameWindow()

pygame.quit()
