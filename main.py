import pygame
from sys import exit
from random import randint
pygame.init()

def displayScore():
    currentTime = int(pygame.time.get_ticks()/1000) - startTime
    scoreSurface = testFont.render(f'Score : {currentTime}',None,(64,64,64))
    scoreRect = scoreSurface.get_rect(center = (400,50))
    screen.blit(scoreSurface, scoreRect)
    return currentTime

def obstacleMovement(obstacleReactList):
    if obstacleReactList:
        for obst in obstacleReactList:
            obst.x = obst.x - 5
            if obst.bottom == 300:
                screen.blit(snailSurface,obst)
            else:
                screen.blit(flySurface,obst)
        obstacleReactList = [obst for   obst in obstacleReactList if obst.x > -100]
        return obstacleReactList
    else:
        return []

def collision(player, obstacles): 
    if obstacles:
        for obst in obstacles:
            if player.colliderect(obst):
                return False
    return True

def playerAnimation():
    global playerSurface, playerIndex

    if playerRect.bottom < 300:
        playerSurface = playerJump
    else:
        playerIndex = playerIndex + 0.1
        if playerIndex >= len(playerWalk):
            playerIndex = 0
        playerSurface = playerWalk[int(playerIndex)]

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Game-101')
clock = pygame.time.Clock()
testFont = pygame.font.Font('font/Pixeltype.ttf', 50)

skySurface = pygame.image.load('graphics/Sky.png').convert()
groundSurface = pygame.image.load('graphics/ground.png').convert()

snailSurface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snailFrame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snailFrames = [snailFrame1,snailFrame2]
snailIndex = 0
snailSurface = snailFrames[snailIndex]

flySurface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
flyFrame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
flyFrame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
flyFrames = [flyFrame1,flyFrame2]
flyIndex = 0
flySurface = flyFrames[flyIndex]

obstacleReactList = []

playerWalk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
playerWalk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
playerIndex = 0
playerWalk = [playerWalk1,playerWalk2]
playerJump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
playerSurface = playerWalk[playerIndex]
playerRect = playerSurface.get_rect(midbottom = (80,300))

#intro scene
playerStand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
playerStand = pygame.transform.rotozoom(playerStand,0, 2)
playerStandRect = playerStand.get_rect(center = (400,200))


playerGravity = 0
gameActive = True
startTime = 0


gameName = testFont.render('Runner',False,(111,196,169))
gameNameRect = gameName.get_rect(center = (400,80))

gameMessage = testFont.render('Press space to Run',False,(111,196,169))
gameMessageRect = gameMessage.get_rect(center = (400,340))
score = 0

#Timer
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer,1500)

snailAnimationTimer = pygame.USEREVENT + 2
pygame.time.set_timer(snailAnimationTimer, 500)

flyAnimationTime = pygame.USEREVENT + 3
pygame.time.set_timer(flyAnimationTime, 200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  
        if gameActive: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playerRect.collidepoint(event.pos) and playerRect.bottom >=300:
                    playerGravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and playerRect.bottom >=300: 
                    playerGravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameActive = True
                startTime = int(pygame.time.get_ticks()/1000)
        if gameActive:  
            if event.type == obstacleTimer:
                if randint(0, 2):
                    obstacleReactList.append(snailSurface.get_rect(midbottom = (randint(900, 1100),300)))
                else:
                    obstacleReactList.append(flySurface.get_rect(midbottom = (randint(900, 1100),210)))
            if event.type == snailAnimationTimer:
                if snailIndex == 0 :
                    snailIndex = 1
                else:
                    snailIndex = 0
                snailSurface = snailFrames[snailIndex]
            if event.type == flyAnimationTime:
                if flyIndex == 0 :
                    flyIndex = 1
                else:
                    flyIndex = 0
                flySurface = flyFrames[flyIndex]
           
    if gameActive:
        #draw all the elements
        screen.blit(skySurface, (0,0))
        screen.blit(groundSurface, (0,300))
        
        score = displayScore()
        
        obstacleReactList = obstacleMovement(obstacleReactList)

        #player
        playerGravity = playerGravity + 1
        playerRect.y = playerRect.y + playerGravity
        if playerRect.bottom >= 300:
            playerRect.bottom = 300
        playerAnimation()
        screen.blit(playerSurface,playerRect)

        # collisions
        gameActive = collision(playerRect,obstacleReactList)

    else:
        screen.fill((94,129,162))
        screen.blit(playerStand,playerStandRect)
        obstacleReactList.clear()
        playerRect.midbottom = (80,300)
        playerGravity = 0

        scoreMsg = testFont.render(f'Your Score is {score}',False,(111,196,169))
        scoreMsgRect = scoreMsg.get_rect(center = (400,330))

        screen.blit(gameName, gameNameRect)
        if score == 0:
            screen.blit(gameMessage, gameMessageRect)
        else:
            screen.blit(scoreMsg, scoreMsgRect)

    pygame.display.update()
    clock.tick(60)