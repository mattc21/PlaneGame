"""
PlaneGame by Matthew Chen.

Note: Some of the names of classes variables may be strange. Just ignore that :p

Things to add:
    -A menu screen.
    -Choose which game to play.
    -Increase difficulty of games (as its pretty easy right now).
"""

import pygame, sys, time
import pygame.freetype
import random

from config import FPS, WINDOWWIDTH, WINDOWHEIGHT, LEFT, RIGHT
from config import WHITE, BLACK, FORESTGREEN, HIGHSCORE, missilenumber, cutscene_played, cutscene_played2
from config import FPSCLOCK, DISPLAYSURF, missilespeed, my_ft_font
from pygame.locals import *


class speed_increase:
    def __init__(self):
        self.start = time.time()
    def myfunc(self):
        global missilespeed
        if time.time() - self.start > 5:
            missilespeed += 1
            self.start = time.time()

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.image.load("missile2.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image,(50, 10))
        self.image = pygame.transform.rotate(self.image, (90))
        self.rect = self.image.get_rect()

    def reset_pos(self):
        #resets position to top of frame
        self.rect.y = random.randrange(-300, -20) #appears off screen
        self.rect.x = random.randrange(0, WINDOWWIDTH)

    def update(self):
        #makes it have a moving functionality
        self.rect.y += missilespeed #moves it down "missilespeed" number of blocks
        if self.rect.y > WINDOWHEIGHT: #resets position if it moves off screen
            self.reset_pos()

class Wolf(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        global wolf_size
        wolf_size = 40
        global wolf_original #it is necessary to create an unscaled image to prevent pixellation when enlarging
        wolf_original = pygame.image.load("bullseye.png").convert_alpha()

        super().__init__()

        self.image = pygame.transform.scale(wolf_original,(wolf_size, wolf_size))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    #def reset_pos(self):
        #currently unused
        #self.rect.y = random.randrange(0, WINDOWHEIGHT)
        #self.rect.x = random.randrange(0, WINDOWWIDTH)

    def update(self):
        global wolf_size, wolf_original
        if wolf_size < 200:
            wolf_size += 1
            self.image = pygame.transform.scale(wolf_original, (wolf_size, wolf_size))
        if wolf_size >= 200 and wolf_size < 1000:
            wolf_size += 2
            self.image = pygame.transform.scale(wolf_original, (wolf_size, wolf_size))
        #this gets the rectangle size as it is updated but does not reset the position to (0,0).
        #essential for allowing it to have positions other than (0,0) which is default
        self.rect = self.image.get_rect(topleft= (self.rect.topleft))

class Coin(pygame.sprite.Sprite):
    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.image.load("coin.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image,(50, 50))
        self.rect = self.image.get_rect()

    def reset_pos(self):
        # Random coins reappear when destroyed
        self.rect.y = random.randrange(0, WINDOWHEIGHT)
        self.rect.x = random.randrange(0, WINDOWWIDTH)
class Star(pygame.sprite.Sprite):
    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.image.load("star.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image,(50, 50))
        self.rect = self.image.get_rect()

class Plane(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.image.load("plane.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image,(20, 24))
        self.rect = self.image.get_rect()

    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Fetch the x and y out of the list,
        # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        self.rect.x = pos[0] - 10
        self.rect.y = pos[1] - 12

    def is_collided_with(self, Block):
        #return self.rect.colliderect(Block.rect)
        return pygame.sprite.spritecollide(self, Block, False)

    def coins_gained(self, Coin):
        #returns True if collision with coins
        return pygame.sprite.spritecollide(self, Coin, False)

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.image.load("crosshair.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image,(50, 50))
        self.rect = self.image.get_rect()

    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Fetch the x and y out of the list,
        # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        self.rect.x = pos[0] - 20
        self.rect.y = pos[1] - 24

def snipe(): 
    #for counting number of wolf kills
    wolf_kills_required = 7
    wolf_kills = 0

    wolf = Wolf(BLACK, 50, 50)
    wolf_list = pygame.sprite.Group()
    wolf_list.add(wolf)
    satania_lmao = pygame.image.load("satania_2.png").convert_alpha()
    satania_lmao_pos = (0,0)
    satania_1 = pygame.image.load("thumbs_up.png")
    crosshair = Crosshair(BLACK, 50, 50)
    crosshair_list = pygame.sprite.Group()
    crosshair_list.add(crosshair)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:  #right mouse button. left mouse buttons is 1.

                #to kill the wolves
                if pygame.sprite.collide_rect(crosshair, wolf) == True:
                #or wolf in clicked_wolves:
                    wolf.kill()

                    #wolf kill counter
                    wolf_kills +=1
                    if wolf_kills == wolf_kills_required:
                        DISPLAYSURF.fill(WHITE)
                        DISPLAYSURF.blit(satania_1, satania_lmao_pos)
                        my_ft_font.render_to(DISPLAYSURF, (600, 340), "You won. Press space to continue.", (BLACK))
                        pygame.display.update()
                        wait()
                        planegame()
                        #wolf_kills = 0

                    wolf = Wolf(BLACK, 50, 50)
                    #random position for wolf spawn
                    wolf.rect.center = (random.randrange(300, WINDOWWIDTH-300), random.randrange(200, WINDOWHEIGHT-200))
                    wolf_list.add(wolf)

        if wolf_size >= 200: #this is the you lose screen
            wolf.kill()
            DISPLAYSURF.fill(WHITE)
            DISPLAYSURF.blit(satania_lmao, satania_lmao_pos)
            my_ft_font.render_to(DISPLAYSURF, (600, 340), "Too slow! Press SPACE to try again.", (BLACK))
            pygame.display.update()
            wait()
            snipe()

        #drawing stuff on the screen and updating it

        DISPLAYSURF.fill(WHITE)
        wolf_list.update()
        wolf_list.draw(DISPLAYSURF)
        crosshair_list.update()
        crosshair_list.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def story_progression():
    global my_ft_font, cutscene_played, cutscene_played2
    if HIGHSCORE > 5 and cutscene_played == False:
        cutscene_played = True
        #setting variables
        mountain = pygame.image.load("mountain2.png").convert_alpha()

        #TEXT AND STUFF FOR STORYLINE
        DISPLAYSURF.fill(BLACK)
        my_ft_font.render_to(DISPLAYSURF, (600, 340), "You passed round one! Press space bar to continue.", (255, 255, 255))
        pygame.display.update()
        wait()
        DISPLAYSURF.fill(BLACK)
        mountain_position = (100, 100)
        satania_position = (0, 0)
        DISPLAYSURF.blit(mountain, (mountain_position))
        my_ft_font.render_to(DISPLAYSURF, (600, 340), "Click on the images that appear!", (255, 255, 255))
        pygame.display.update()
        time.sleep(1)
        wait()
        DISPLAYSURF.fill(BLACK)
        my_ft_font.render_to(DISPLAYSURF, (600, 340), "Press space to start.", (255, 255, 255))
        pygame.display.update()
        wait()
        snipe()

    elif HIGHSCORE > 20 and cutscene_played2 == False:
        cutscene_played2 = True
        DISPLAYSURF.fill(BLACK)
        my_ft_font.render_to(DISPLAYSURF, (600, 340), "You passed round two! Please wait as the next stage does not exist yet. For now, press space to continue.", (255, 255, 255))
        pygame.display.update()
        wait()

def main():

    global FPSCLOCK, DISPLAYSURF, HIGHSCORE, my_ft_font
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    my_ft_font = pygame.freetype.SysFont('Times New Roman', 15)
    planegame()

def planegame():
    global FPSCLOCK, DISPLAYSURF, missilespeed, missilenumber, HIGHSCORE, my_ft_font
    missilespeed = 3.0
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BGCOLOUR = (60, 60, 100, 100)
    points = 0
    pygame.display.set_caption('Plane Game')
    is_collided = False
    block_list = pygame.sprite.Group() #making groups
    all_sprites_list = pygame.sprite.Group()
    coins_created = False
    coin_list = pygame.sprite.Group() #making groups
    stars_created = False
    star_list = pygame.sprite.Group() #making groups
    for i in range(missilenumber):
        #this represents a missile
        missile = Block(BLACK, 20, 15)
        # Set a random location for the block. Makes it appear off map.
        missile.rect.x = random.randrange(WINDOWWIDTH)
        missile.rect.y = random.randrange(WINDOWHEIGHT) - WINDOWHEIGHT

        # Add the block to the list of objects
        block_list.add(missile)
        all_sprites_list.add(missile)

    #create a plane
    plane = Plane(BLACK, 20, 15)
    all_sprites_list.add(plane)

    speedup = speed_increase()
    while True: #main game loop

        speedup.myfunc()

        for missile in block_list:
            if missile.rect.y > WINDOWHEIGHT-1 and coins_created == False:
                for i in range (5):
                    #this represents a coin
                    coin = Coin(BLACK, 20, 15)
                    # Set a random location for the coin
                    coin.rect.x = random.randrange(WINDOWWIDTH-50)
                    coin.rect.y = random.randrange(WINDOWHEIGHT-50)
                    coin_list.add(coin)
                    all_sprites_list.add(coin)
                    coins_created = True


        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE and is_collided == True:
                    planegame()


        # Calls update() method on every sprite in the list
        all_sprites_list.update()

        # See if the player block has collided with anything.
        # pygame.sprite.spritecollide(block_list, plane, True)
        if plane.is_collided_with(block_list):
                plane.kill()
                is_collided = True

        if points > HIGHSCORE:
            HIGHSCORE = points


        coin_hit_list = pygame.sprite.spritecollide(plane, coin_list, False)
        for coin in coin_hit_list:
            points += 1
            coin.reset_pos()
            if random.randrange(1,5)>1 and stars_created == False:

                #this represents a missile
                star = Star(BLACK, 20, 15)
                # Set a random location for the block. Makes it appear off map.
                star.rect.x = random.randrange(WINDOWWIDTH-50)
                star.rect.y = random.randrange(WINDOWHEIGHT-50)

                # Add the block to the list of objects
                star_list.add(star)
                all_sprites_list.add(star)
                stars_created = True


        star_hit_list = pygame.sprite.spritecollide(plane, star_list, False)

        if not star_list:
            stars_created = False

        for star in star_hit_list:
                star.kill()
                if missilespeed > 1:
                    missilespeed -= 1
        DISPLAYSURF.fill(WHITE)
        all_sprites_list.draw(DISPLAYSURF)
        if is_collided == True:
            my_ft_font.render_to(DISPLAYSURF, (600, 340), "Collision! You lose! Press space bar to continue.", (0, 0, 0))

        my_ft_font.render_to(DISPLAYSURF, (10, 10), f"Points: %s Highscore: {HIGHSCORE} Missile Speed: {missilespeed} " %points, (0, 0, 0))
        story_progression()
        pygame.display.update()
        FPSCLOCK.tick(FPS)




if __name__ == '__main__':
    main()
