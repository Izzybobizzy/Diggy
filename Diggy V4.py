##################
###PREGAME CODE###
##################

###IMPORTS AND INITIALIZATIONS
import pygame
from time import sleep
import math
# Is used to help locate and load files/assets
import os
from os.path import isfile, join

pygame.mixer.init()
pygame.init()
pygame.font.init()

###WINDOW DISPLAY SETUP
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
NAME = pygame.display.set_caption("Diggy's Dungeon Disaster")
FPS = 60

###ASSETS
# Fonts
HEALTH_BAR_FONT = pygame.font.SysFont("elixIR", 17)

# Images
BACKGROUND = pygame.image.load("Cave dungion.png")
FAIL_SCREEN = pygame.image.load("DIGGY_DIED.png")
ESCAPE_SCREEN = pygame.image.load("DIGGY_ESCAPED.png")
wall = pygame.image.load("cave wall.png")
base_diggy = pygame.image.load("My Digging Friend.png")
floor = pygame.image.load("cave floor.png")
spike = pygame.image.load("cave spike design.png")
floor_spike = pygame.image.load("F_SPIKE.png")
DOOR = pygame.image.load("Door.png")

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80

# Transformed images
OFF_DIGGY = pygame.transform.scale(base_diggy, (PLAYER_WIDTH, PLAYER_HEIGHT))
LONG_WALL = pygame.transform.scale(wall, (188, 700))
SPIKE = pygame.transform.scale(spike, (28, 100))

#Music
music = pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Game sound affects
HURT_SFX = pygame.mixer.Sound("Ouchie_audio.mp3")
SPIKE_DETACH_SFX = pygame.mixer.Sound("spike_detach.mp3")
WALK_SFX = pygame.mixer.Sound("walking_sfx.mp3")
DEATH_SFX = pygame.mixer.Sound("death_sfx.mp3")

# All colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Player:
    def __init__(self, png, x, y, radius, colour, vel_a, vel_d, gravity, jump_count):
        self.png = png
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel_a = vel_a
        self.vel_d = vel_d
        self.gravity = gravity
        self.jump = False
        self.jump_count = jump_count

    # create the player
    def create(self):
        pygame.draw.circle(WINDOW, self.colour, (self.x, self.y), self.radius)
        WINDOW.blit(self.png, (self.x - (self.radius + self.radius / 2), self.y - self.radius))


class HealthBar:
    def __init__(self, health_num, width):
        self.health_num = health_num
        self.width = width

    # create the health bar
    def spawn_health(self):
        bar_text = HEALTH_BAR_FONT.render("Health: ", 1, WHITE)
        health = HEALTH_BAR_FONT.render(f"{self.health_num}", 1.7, WHITE)
        WINDOW.blit(bar_text, (100, 25))
        WINDOW.blit(health, (175, 25))
        health_bar = pygame.draw.rect(WINDOW, RED, (100, 50, self.width, 25))

    # reset the players health bar to max
    def reset_health(self):
        self.width = 100
        self.health_num = 100


class Background:
    def __init__(self, png, x, y, x_vel):
        self.png = png
        self.x = x
        self.y = y
        self.x_vel = x_vel

    # create the background
    def create(self):
        WINDOW.blit(self.png, (self.x, self.y))


class Block:
    def __init__(self, png, x, y, width, height, x_vel, rep):
        self.png = png
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_vel = x_vel
        self.rep = rep

    # create the block
    def create(self):
        pygame.draw.rect(WINDOW, WHITE, (self.x, self.y, self.width, self.height))

    #paste the image 1 or more times onto the block
    def mask(self):
        displacement = 0
        for i in range(self.rep):
            WINDOW.blit(self.png, (self.x + displacement, self.y))
            displacement += 174

    #create the door to escape
    def escape_door(self):
        pygame.draw.rect(WINDOW, BLACK, (self.x, self.y, self.width, self.height))

        WINDOW.blit(self.png, (self.x - 240, self.y + 10))

class Spikes:
    def __init__(self, png, x, y, width, height, colour, x_vel, fall_vel):
        self.png = png
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.x_vel = x_vel
        self.fall_vel = fall_vel

    # create the falling spike
    def create(self):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, self.width, self.height))

        WINDOW.blit(self.png, (self.x - 10, self.y))

    def reset_vel(self):
        self.fall_vel = 25

class FloorSpikes():
    def __init__(self, png, x, y, width, height, colour, x_vel):
        self.png = png
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.x_vel = x_vel

        #create the floor spike
    def create(self):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, self.width, self.height))

        WINDOW.blit(self.png, (self.x - 6, self.y - 25))

class CheckPoint:
    def __init__(self, x, y, radius, x_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = x_vel

    #create the check point
    def create(self):
        pygame.draw.circle(WINDOW, RED, (self.x, self.y), self.radius)

# move any object to the right while charcter moves left
def move_left(object, move=True):

    object.x -= object.x_vel

    if move == False:
        object.x -= 0

# move any object to the left while character moves to the right
def move_right(object, move=True):

    object.x += object.x_vel

    if move == False:
        object.x += 0

# function for any falling spike interacting with the character
def falling_spike_collision(spike, char,check, h_bar):

    #move checkpoint off the bottom of the screen when the character passes it
    if check.x <= char.x:
        check.y += 200

    #After the check point moves off screen (instantaniously)
    if check.y > 700:

        #let the spike fall
        spike.y += spike.fall_vel
        spike.fall_vel += 13


    #when the spike collides with the character (y - coordinate)
    if (spike.y >= (char.y - char.radius)) and (spike.y <= (char.y + 60)):
        #when the spike collides with the character (x - coordinate)
        if ((char.x + char.radius) >= spike.x) and ((char.x - char.radius) <= (spike.x + spike.width)):

            #deal damage to character
            h_bar.width -= 25
            h_bar.health_num -= 25
            HURT_SFX.play()

# function for when charcter collides with floor spikes
def floor_spike_collision(floorspike, char, h_bar):
    ## if the player collides with spike
    if (char.x + char.radius) >= floorspike.x and (char.x - char.radius) <= (floorspike.x + floorspike.width):
        if ((char.y + char.radius) + 60) >= (floorspike.y):
            h_bar.width -= 1

#function to reset the postion of the given object
def reset_object(object, x , y):

    #reset given object using given coordinates
    object.create()

    #reset the objects x and y coordintes to reset movement
    object.x = x
    object.y = y


#main game
def main():

    # Player
    ball = Player(OFF_DIGGY, 600, WINDOW_HEIGHT - 135, 20, WHITE, 12, 12, 1, 7)

    # Background of game
    setting = Background(BACKGROUND, 0, 0, 10)

    # Left wall at begining
    wall_one = Block(LONG_WALL, 0, 0, 188, 700, 10, 1)

    # Second wall that placed before the left wall
    wall_two = Block(LONG_WALL, -188, 0, 188, 700, 10, 1)

    #Wall on right side of map where the exit is
    wall_three = Block(LONG_WALL, 3700, 0, 188, 700, 10, 1)

    #The escape door
    door = Block(DOOR,3700, 500, 1,100,10, 1)

    #All falling and non-falling spikes
    spike1 = Spikes(SPIKE, 547, 0, 10, 80, BLACK, 10, 25)
    spike2 = Spikes(SPIKE,600, 0, 10, 80, BLACK, 10, 25)
    spike3 = Spikes(SPIKE,786, 0, 10, 80, BLACK, 10, 25)
    spike4 = Spikes(SPIKE,814, 0, 10, 80, BLACK, 10, 25)
    spike5 = Spikes(SPIKE,888, 0, 10, 80, BLACK, 10, 25)
    spike6 = Spikes(SPIKE,929, 0, 10, 80, BLACK, 10, 25)
    spike7 = Spikes(SPIKE,998, 0, 10, 80, BLACK, 10, 25)
    spike8 = Spikes(SPIKE,1028, 0, 10, 80, BLACK, 10, 25)
    spike9 = Spikes(SPIKE,1100, 0, 10, 80, BLACK, 10, 25)
    spike10 = Spikes(SPIKE,1168, 0, 10, 80, BLACK, 10, 25)
    spike11 = Spikes(SPIKE,1209, 0, 10, 80, BLACK, 10, 25)
    spike12 = Spikes(SPIKE,1304, 0, 10, 80, BLACK, 10, 25)
    spike13 = Spikes(SPIKE,1399, 0, 10, 80, BLACK, 10, 25)
    spike14 = Spikes(SPIKE,1484, 0, 10, 80, BLACK, 10, 25)
    spike15 = Spikes(SPIKE,1563, 0, 10, 80, BLACK, 10, 25)
    spike16 = Spikes(SPIKE, 1664, 0, 10, 80, BLACK, 10, 25)
    spike17 = Spikes(SPIKE, 1811, 0, 10, 80, BLACK, 10, 25)
    spike18 = Spikes(SPIKE, 1900, 0, 10, 80, BLACK, 10, 25)
    spike19 = Spikes(SPIKE, 2001, 0, 10, 80, BLACK, 10, 25)
    spike20 = Spikes(SPIKE, 2099, 0, 10, 80, BLACK, 10, 25)
    spike21 = Spikes(SPIKE, 2152, 0, 10, 80, BLACK, 10, 25)
    spike22 = Spikes(SPIKE, 2271, 0, 10, 80, BLACK, 10, 25)
    spike23 = Spikes(SPIKE, 2299, 0, 10, 80, BLACK, 10, 25)
    spike24 = Spikes(SPIKE, 2331, 0, 10, 80, BLACK, 10, 25)
    spike25 = Spikes(SPIKE, 2399, 0, 10, 80, BLACK, 10, 25)
    spike26 = Spikes(SPIKE, 2471, 0, 10, 80, BLACK, 10, 25)
    spike27 = Spikes(SPIKE, 2572, 0, 10, 80, BLACK, 10, 25)
    spike28 = Spikes(SPIKE, 2621, 0, 10, 80, BLACK, 10, 25)
    spike29 = Spikes(SPIKE, 2700, 0, 10, 80, BLACK, 10, 25)
    spike30 = Spikes(SPIKE, 2789, 0, 10, 80, BLACK, 10, 25)
    spike31 = Spikes(SPIKE, 2850, 0, 10, 80, BLACK, 10, 25)
    spike32 = Spikes(SPIKE, 2926, 0, 10, 80, BLACK, 10, 25)
    spike33 = Spikes(SPIKE, 2999, 0, 10, 80, BLACK, 10, 25)
    spike34 = Spikes(SPIKE, 3041, 0, 10, 80, BLACK, 10, 25)
    spike35 = Spikes(SPIKE, 3152, 0, 10, 80, BLACK, 10, 25)
    spike36 = Spikes(SPIKE, 3198, 0, 10, 80, BLACK, 10, 25)
    spike37 = Spikes(SPIKE, 3278, 0, 10, 80, BLACK, 10, 25)
    spike38 = Spikes(SPIKE, 3333, 0, 10, 80, BLACK, 10, 25)
    spike39 = Spikes(SPIKE, 3479, 0, 10, 80, BLACK, 10, 25)
    spike40 = Spikes(SPIKE, 3542, 0, 10, 80, BLACK, 10, 25)


    #corrseponding checkpoints for each of the falling spikes
    spike5_check = CheckPoint(spike5.x - 70, 600, 1, 10)
    spike8_check = CheckPoint(spike8.x - 70, 600, 1, 10)
    spike10_check = CheckPoint(spike10.x - 70, 600, 1, 10)
    spike14_check = CheckPoint(spike14.x - 70, 600, 1, 10)
    spike18_check = CheckPoint(spike18.x - 70, 600, 1, 10)
    spike24_check = CheckPoint(spike24.x - 70, 600, 1, 10)
    spike28_check = CheckPoint(spike28.x - 70, 600, 1, 10)
    spike33_check = CheckPoint(spike33.x - 70, 600, 1, 10)
    spike38_check = CheckPoint(spike38.x - 70, 600, 1, 10)
    spike39_check = CheckPoint(spike39.x - 70, 600, 1, 10)



    # Player health bar
    player_health = HealthBar(100, 100)

    # Check point on left side of map
    front_check = CheckPoint(250, 600, 10, 10)

    # Check point on right side of map
    back_check = CheckPoint(3550, 600, 10, 10)

    # main floor
    floor_one = Block(floor, -100, WINDOW_HEIGHT - 75, 8000, 200, 20, 40)

    run = True

    while run:

        #delay game by 50 milaseconds
        pygame.time.delay(50)

        #create background
        setting.create()

        #analyze when keys get pressed
        keys = pygame.key.get_pressed()

        #move character to the left when the a key is pressed
        if keys[pygame.K_a]:

            ball.x -= ball.vel_a

            #if the charcter moves to the right side of the screen before hiting the check point
            if ((ball.x - ball.radius) <= 260) and ((ball.x - ball.radius) > front_check.x):

                #character will stop at x = 260, while objects move in the opposite direction
                ball.vel_a = 0
                ball.vel_d = 12


                move_right(setting)

                move_right(spike1)
                move_right(spike2)
                move_right(spike3)
                move_right(spike4)
                move_right(spike5)
                move_right(spike6)
                move_right(spike7)
                move_right(spike8)
                move_right(spike9)
                move_right(spike10)
                move_right(spike11)
                move_right(spike12)
                move_right(spike13)
                move_right(spike14)
                move_right(spike15)
                move_right(spike16)
                move_right(spike17)
                move_right(spike18)
                move_right(spike19)
                move_right(spike20)
                move_right(spike21)
                move_right(spike22)
                move_right(spike23)
                move_right(spike24)
                move_right(spike25)
                move_right(spike26)
                move_right(spike27)
                move_right(spike28)
                move_right(spike29)
                move_right(spike30)
                move_right(spike31)
                move_right(spike32)
                move_right(spike33)
                move_right(spike34)
                move_right(spike35)
                move_right(spike36)
                move_right(spike37)
                move_right(spike38)
                move_right(spike39)
                move_right(spike40)



                move_right(wall_one)
                move_right(wall_two)
                move_right(wall_three)
                move_right(door)

                move_right(front_check)
                move_right(back_check)

                move_right(spike5_check)
                move_right(spike8_check)
                move_right(spike10_check)
                move_right(spike14_check)
                move_right(spike18_check)
                move_right(spike24_check)
                move_right(spike28_check)
                move_right(spike33_check)
                move_right(spike38_check)
                move_right(spike39_check)

                move_right(floor_one)

                #when the character moves past the check point on the left side of the map
                if ((ball.x - ball.radius) <= front_check.x):
                    ball.vel_a = 12
                    ball.vel_d = 12

            # if the charcter is in the middle part of the screen (between 260 - 940)
            if (ball.x > 260) and (ball.x < 940):
                ball.vel_a = 12
                ball.vel_d = 12

            #if the character touches the wall on the left side of the map
            if (ball.x - ball.radius) <= (wall_one.x + wall_one.width):
                ball.vel_a = 0
                ball.vel_d = 12

        #move character to the right when the d key is pressed
        if keys[pygame.K_d]:

            ball.x += ball.vel_d

            if ((ball.x + ball.radius) >= 940) and ((ball.x + ball.radius) < back_check.x):

                # character will stop at x = 940, while objects move in the opposite direction
                ball.vel_a = 12
                ball.vel_d = 0


                move_left(setting)

                move_left(spike1)
                move_left(spike2)
                move_left(spike3)
                move_left(spike4)
                move_left(spike5)
                move_left(spike6)
                move_left(spike7)
                move_left(spike8)
                move_left(spike9)
                move_left(spike10)
                move_left(spike11)
                move_left(spike12)
                move_left(spike13)
                move_left(spike14)
                move_left(spike15)
                move_left(spike16)
                move_left(spike17)
                move_left(spike18)
                move_left(spike19)
                move_left(spike20)
                move_left(spike21)
                move_left(spike22)
                move_left(spike23)
                move_left(spike24)
                move_left(spike25)
                move_left(spike26)
                move_left(spike27)
                move_left(spike28)
                move_left(spike29)
                move_left(spike30)
                move_left(spike31)
                move_left(spike32)
                move_left(spike33)
                move_left(spike34)
                move_left(spike35)
                move_left(spike36)
                move_left(spike37)
                move_left(spike38)
                move_left(spike39)
                move_left(spike40)

                move_left(wall_one)
                move_left(wall_two)
                move_left(wall_three)
                move_left(door)

                move_left(front_check)
                move_left(back_check)

                move_left(spike5_check)
                move_left(spike8_check)
                move_left(spike10_check)
                move_left(spike14_check)
                move_left(spike18_check)
                move_left(spike24_check)
                move_left(spike28_check)
                move_left(spike33_check)
                move_left(spike38_check)
                move_left(spike39_check)

                move_left(floor_one)

            # if the charcter is in the middle part of the screen (between 260 - 940)
            if (ball.x > 260) and (ball.x < 940):
                ball.vel_a = 12
                ball.vel_d = 12

            # if the chacter moves past the checkpoint of the right side of the map,
            # only let the character to be able to move
            if ((ball.x + ball.radius) >= back_check.x):
                ball.vel_a = 12
                ball.vel_d = 12

        if not (ball.jump):

            if keys[pygame.K_SPACE]:
                ball.jump = True

        else:
            if ball.jump_count >= -7:
                ball.y -= (ball.jump_count * abs(ball.jump_count))
                ball.jump_count -= 1

            else:
                ball.jump_count = 7
                ball.jump = False

        #create all in game objects, including player
        ball.create()

        wall_one.create()
        wall_two.create()
        wall_three.create()
        wall_one.mask()
        wall_two.mask()
        wall_three.mask()

        door.escape_door()

        floor_one.create()
        floor_one.mask()

        spike1.create()
        spike2.create()
        spike3.create()
        spike4.create()
        spike5.create()
        spike6.create()
        spike7.create()
        spike8.create()
        spike9.create()
        spike10.create()
        spike11.create()
        spike12.create()
        spike13.create()
        spike14.create()
        spike15.create()
        spike16.create()
        spike17.create()
        spike18.create()
        spike19.create()
        spike20.create()
        spike21.create()
        spike22.create()
        spike23.create()
        spike24.create()
        spike25.create()
        spike26.create()
        spike27.create()
        spike28.create()
        spike29.create()
        spike30.create()
        spike31.create()
        spike32.create()
        spike33.create()
        spike34.create()
        spike35.create()
        spike36.create()
        spike37.create()
        spike38.create()
        spike39.create()
        spike40.create()

        falling_spike_collision(spike5, ball, spike5_check, player_health)
        falling_spike_collision(spike8, ball, spike8_check, player_health)
        falling_spike_collision(spike10, ball, spike10_check, player_health)
        falling_spike_collision(spike14, ball, spike14_check, player_health)
        falling_spike_collision(spike18, ball, spike18_check, player_health)
        falling_spike_collision(spike24, ball, spike24_check, player_health)
        falling_spike_collision(spike28, ball, spike28_check, player_health)
        falling_spike_collision(spike33, ball, spike33_check, player_health)
        falling_spike_collision(spike38, ball, spike38_check, player_health)
        falling_spike_collision(spike39, ball, spike39_check, player_health)


        player_health.spawn_health()

        #blit the death screen when the player dies
        if player_health.width <= 0:

            pygame.mixer.music.stop()

            WINDOW.blit(FAIL_SCREEN, (0,0))

            # if the player clicks r to replay the game, rest everything in their
            # original postion and restart the music
            if keys[pygame.K_r]:

                reset_object(ball, 600, WINDOW_HEIGHT - 135)
                reset_object(wall_one, 0,0)
                reset_object(wall_two, -188, 0)
                reset_object(wall_three, 3700, 0)

                reset_object(spike1, 547, 0)
                reset_object(spike2, 600, 0)
                reset_object(spike3, 786, 0)
                reset_object(spike4, 814, 0)
                reset_object(spike5, 888, 0)
                reset_object(spike6, 929, 0)
                reset_object(spike7, 998, 0)
                reset_object(spike8, 1028, 0)
                reset_object(spike9, 1100, 0)
                reset_object(spike10, 1168, 0)
                reset_object(spike11, 1209, 0)
                reset_object(spike12, 1304, 0)
                reset_object(spike13, 1399, 0)
                reset_object(spike14, 1484, 0)
                reset_object(spike15, 1563, 0)
                reset_object(spike16, 1664, 0)
                reset_object(spike17, 1811, 0)
                reset_object(spike18, 1900, 0)
                reset_object(spike19, 2001, 0)
                reset_object(spike20, 2099, 0)
                reset_object(spike21, 2152, 0)
                reset_object(spike22, 2271, 0)
                reset_object(spike23, 2299, 0)
                reset_object(spike24, 2331, 0)
                reset_object(spike25, 2399, 0)
                reset_object(spike26, 2471, 0)
                reset_object(spike27, 2572, 0)
                reset_object(spike28, 2621, 0)
                reset_object(spike29, 2700, 0)
                reset_object(spike30, 2789, 0)
                reset_object(spike31, 2850, 0)
                reset_object(spike32, 2926, 0)
                reset_object(spike33, 2999, 0)
                reset_object(spike34, 3041, 0)
                reset_object(spike35, 3152, 0)
                reset_object(spike36, 3198, 0)
                reset_object(spike37, 3278, 0)
                reset_object(spike38, 3333, 0)
                reset_object(spike39, 3479, 0)
                reset_object(spike40, 3542, 0)

                reset_object(front_check, 250, 600)
                reset_object(back_check, 3550, 600)

                reset_object(spike5_check, spike5.x - 70, 600)
                reset_object(spike8_check, spike8.x - 70, 600)
                reset_object(spike10_check, spike10.x - 70, 600)
                reset_object(spike14_check, spike14.x - 70, 600)
                reset_object(spike18_check, spike18.x - 70, 600)
                reset_object(spike24_check, spike24.x - 70, 600)
                reset_object(spike28_check, spike28.x - 70, 600)
                reset_object(spike33_check, spike33.x - 70, 600)
                reset_object(spike38_check, spike38.x - 70, 600)
                reset_object(spike39_check, spike39.x - 70, 600)

                reset_object(floor_one, -100, WINDOW_HEIGHT - 75)

                spike5.reset_vel()
                spike8.reset_vel()
                spike10.reset_vel()
                spike14.reset_vel()
                spike18.reset_vel()
                spike24.reset_vel()
                spike28.reset_vel()
                spike33.reset_vel()
                spike38.reset_vel()
                spike39.reset_vel()

                pygame.mixer.music.play(-1)

                player_health.reset_health()

        #when the character makes it to the end, blit the escaped screen
        if (ball.x + ball.radius) >= wall_three.x:

            pygame.mixer.music.stop()
            WINDOW.blit(ESCAPE_SCREEN, (0, 0))


        pygame.display.update()


        # Close the game when the user clicks the "x" in the corner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


print(main())