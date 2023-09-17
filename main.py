# Example file showing a basic pygame "game loop"
import pygame
import random
pygame.init()
pygame.display.set_icon(pygame.image.load("dino1.png"))
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Python Dinosaur")
clock = pygame.time.Clock()
running = True
ground = pygame.image.load("suelo.png")
cloud = pygame.image.load("nube.png")
dinoWalking = [ pygame.image.load("dino1.png"), pygame.image.load("dino2.png"),pygame.image.load("dino3.png")]
cactus1 = pygame.image.load("cactus1.png")
cactus2 = pygame.image.load("cactus2.png")
dinoDead = pygame.image.load("dinoDead.png")

gravity = 1
class Dino():
    def __init__(self):
        self.image = dinoWalking[0]
        self.rect = self.image.get_rect(topleft = (256, 636))
        self.rect.move(256, 636)
        self.rect.width -= 15
        self.rect.height -= 15
        self.walkingState = 0
        self.canJump = True
        # self.rect.x = 0
        # self.rect.y = 636
        self.y_velocity = 0
        self.jumping = False

class Ground():
    def __init__(self):
        self.image = ground
        self.rect = self.image.get_rect(topleft = (0, 678))
        # self.rect.x = 0
        # self.rect.y = 678

class Cloud():
    def __init__(self):
        self.image = pygame.image.load("nube.png")
        yPos = random.randint(200, 360)
        self.rect = self.image.get_rect(topleft = (1280, yPos))

class Cactus():
    def __init__(self):
        prob = round(random.random() * 100)
        self.x = 1280
        if prob <= 50:
            self.image = pygame.image.load("cactus1.png")
            self.rect = self.image.get_rect(topleft = (1280, 720 - 96))
            self.rect.move(1280, 720 - 96)
            self.width = 46 
            self.heigth = 96 
            # self.rect.y = 720 - 96
        else:
            self.image = pygame.image.load("cactus2.png")
            self.rect = self.image.get_rect(topleft = (1280, 720 - 70))
            self.rect.move(1280, 720 - 70)
            self.width = 98 
            self.heigth = 66 
            # self.rect.y = 720 - 70

dino = Dino()
ground0 = Ground()
ground1 = Ground()
ground1.rect.x = 1280

groundVel = 10
gameVel = 0
cloudVel = 3.4
clouds: list[Cloud] = []
cactus: list[Cactus] = []
cactusColliders = []
gameOver = False

createCloudEvent = pygame.USEREVENT + 1
pygame.time.set_timer(createCloudEvent, 1000)

updateDinoSpriteEvent = pygame.USEREVENT + 2
pygame.time.set_timer(updateDinoSpriteEvent, 100)

createCactusEvent = pygame.USEREVENT + 3
pygame.time.set_timer(createCactusEvent, 1000)

upGameSpeedEvent = pygame.USEREVENT + 4
pygame.time.set_timer(upGameSpeedEvent, 20000)

timeChangeEvent = pygame.USEREVENT + 5
pygame.time.set_timer(timeChangeEvent, 40000)

def updateDinoSprite():
    if not(gameOver):
        dino.image = dinoWalking[dino.walkingState]
    else: 
        dino.image = dinoDead
    if dino.walkingState + 1 > 2: 
        dino.walkingState = 0
    dino.walkingState += 1
    
dayTime = 0 # dia 0, noche 1

def moveDino():
    
    dino.y_velocity -= gravity
    pressed_keys = pygame.key.get_pressed()
    
    if (pygame.mouse.get_pressed()[0] == True or pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]) and dino.canJump and not(gameOver): 
        dino.y_velocity = 20
        dino.rect.y -= 1
        dayTime == 1
        dino.canJump = False
        # 636      678
    elif (pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]): 
        dayTime == 0
        dino.y_velocity = -20
    dino.rect.y -= dino.y_velocity if dino.rect.y + 84 < ground0.rect.y + 42 and not(gameOver) else 0
    if dino.rect.y + 84 >= ground0.rect.y + 42:
        dino.rect.y = 720 - 84
        dino.canJump = True

def set_color(width, height, color):
    for x in range(width):
        for y in range(height):
            screen.set_at((x, y), color)

while running:

    moveDino()

    if pygame.event.get(createCloudEvent):
        prob = round(random.random() * 100)
        if prob <= 50:
            clouds.append(Cloud())

    if pygame.event.get(updateDinoSpriteEvent):
        updateDinoSprite()

    if pygame.event.get(createCactusEvent):
        prob = round(random.random() * 100)
        if prob <= 50:
            cact = Cactus()
            cactus.append(cact)

    if pygame.event.get(upGameSpeedEvent):
        gameVel += 1

    if pygame.event.get(timeChangeEvent):
        print(dayTime)
        if dayTime == 0:
            dayTime = 1
        else:
            dayTime = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDERIZADO

    screen.fill((180, 226, 244) if dayTime == 0 else (28, 33, 33))

    pressed_keys = pygame.key.get_pressed()

    if gameOver and (pygame.mouse.get_pressed()[0] == True or pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]):
        gameOver = False
        dino.rect.y = 720 - 84
        cactus.clear()

    for c in clouds:
        if not(gameOver):
            c.rect.x -= (1 * cloudVel + gameVel)
        if c.rect.x < 0 - c.rect.width:
            clouds.remove(c)
        screen.blit(c.image, c.rect)
    
    screen.blit(ground0.image, ground0.rect)
    screen.blit(ground1.image, ground1.rect)

    if ground0.rect.x <= -1280:
        ground0.rect.x = 0
    if ground1.rect.x <= 0:
        ground1.rect.x = 1280

    if not(gameOver):
        ground0.rect.x -= (1 * groundVel + gameVel)
        ground1.rect.x -= (1 * groundVel + gameVel)

    if len(cactus) > 0:
        if pygame.Rect.colliderect(cactus[0].rect, dino.rect):
            gameOver = True

    if len(cactus) > 0:
        for cact in cactus:
            if not(gameOver):
                cact.rect.x -= (1 * groundVel + gameVel)
                cact.x -= (1 * groundVel + gameVel)
            if (cact.rect.x < 0 - cact.width):
                cactus.remove(cact)
            screen.blit(cact.image, (cact.x, cact.rect.y))

    screen.blit(dino.image, dino.rect)

    pygame.display.flip()
    clock.tick(60) 
    
pygame.quit()