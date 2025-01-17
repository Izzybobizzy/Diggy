##################
###PREGAME CODE###
##################



###IMPORTS AND INITIALIZATIONS
import pygame
from time import sleep
import math
#Is used to help locate and load files/assets
import os
from os.path import isfile, join

pygame.init()
pygame.font.init()



###WINDOW DISPLAY SETUP
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
NAME = pygame.display.set_caption("Diggy's Dungeon Disaster")

FPS = 60



###ASSETS
#Fonts
HEALTH_BAR_FONT = pygame.font.SysFont("vladimirscript", 17)

#Images
BACKGROUND = pygame.image.load(join("assets", "Background", "Cave Dungeon.png"))
wall = pygame.image.load(join("assets", "Background", "cave wall.png"))
base_diggy = pygame.image.load(join("assets", "Characters", "Diggy", "Diggy.png"))
floor = pygame.image.load(join("assets", "Background", "cave floor.png"))
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
#Transformed images
OFF_DIGGY = pygame.transform.scale(base_diggy, (PLAYER_WIDTH, PLAYER_HEIGHT))
LONG_WALL = pygame.transform.scale(wall, (188, 700))

#All colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



class Player:

    def __init__(self, png, x, y ,radius, colour, vel_a, vel_d, gravity, jump_count):
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

    def create(self, x , y):
        pygame.draw.circle(WINDOW, self.colour, (x , y), self.radius)

        WINDOW.blit(self.png, (self.x - (self.radius + self.radius/2), self.y - self.radius))

class HealthBar():

    def __init__(self, health_num):
        self.health_num = health_num

    def spawn_health(self):
        bar_text = HEALTH_BAR_FONT.render("Health: ", 1, WHITE)
        health = HEALTH_BAR_FONT.render("100", 1.7, WHITE)

        WINDOW.blit(bar_text, (100, 25))

        WINDOW.blit(health, (175, 25))

        health_bar = pygame.draw.rect(WINDOW, RED, (100, 50, 100, 25))


class Background:

    def __init__(self, png, x, y, x_vel):
        self.png = png
        self.x = x
        self.y = y
        self.x_vel = x_vel

    def create(self, x , y):
        WINDOW.blit(self.png, (x , y))

class Block:

    def __init__(self, png, x, y, width, height, x_vel, rep):
        self.png = png
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_vel = x_vel
        self.rep = rep

    def create(self, x , y):
        pygame.draw.rect(WINDOW, WHITE, (x , y, self.width, self.height))
    
    def mask(self):
        displacement = 0
        for i in range(self.rep):
            WINDOW.blit(self.png, (self.x + displacement, self.y))
            displacement += 174



class Spikes:

    def __init__(self, x, y, width, height, fall_vel, colour, x_vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fall_vel = fall_vel
        self.colour = colour
        self.x_vel = x_vel


    def create(self, x , y):
        pygame.draw.rect(WINDOW, self.colour, (x , y, self.width, self.height))


class CheckPoint():

    def __init__(self, x, y, radius, x_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = x_vel

    def create(self, x , y):
        pygame.draw.circle(WINDOW, RED, (x , y), self.radius)

#move any object to the left
def move_left(object, move=True):

    object.x -= object.x_vel

    if move == False:
        object.x -= (object.x_vel * 0)

#move any object to the right
def move_right(object, move=True):

    object.x += object.x_vel

    if move == False:
        object.x += (object.x_vel * 0)





#function for any falling spike interacting with the character
def falling_spike_collision(spike, char, h_bar):

    distance = 60

    if ((char.x + char.radius) + distance) >= spike.x:

        distance = 200

        spike.y += spike.fall_vel
        spike.fall_vel += 7

    if spike.y > 700:
        ditance = 60

    if (spike.x >= (char.x - char.radius)) and (spike.x <= (char.x + char.radius)):
        if (char.y + char.radius):
            pass


def main():

    clock = pygame.time.Clock()

    #Player
    ball = Player(OFF_DIGGY, 600, WINDOW_HEIGHT - 135, 20, WHITE, 10, 10, 1, 7)

    #Background of game
    setting = Background(BACKGROUND, 0, 0, 10)

    #Left wall at begining
    wall_one = Block(LONG_WALL, 0, 0, 188, 700, 10, 1)

    #Second wall that placed before the left wall
    wall_two = Block(LONG_WALL, -188, 0, 188, 700, 10, 1)

    #temporary spike
    spike_test = Spikes(800,0, 10, 80, 25, BLACK, 10)

    #Players health bar
    player_health = HealthBar(100)

    #Check point to start objects from moving at the start
    front_check = CheckPoint(250, 600, 10, 10)

    #Check point to start objects from moving at the end
    back_check = CheckPoint(3550, 600, 10, 10)

    #I NEED A FLOOR
    floor_one = Block(floor, 0, WINDOW_HEIGHT - 75, 4000, 200, 20, 5)

    run = True

    while run:

        clock.tick(FPS)

        pygame.time.delay(50)

        setting.create(setting.x, setting.y)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:

            ball.x -= ball.vel_a

            if (ball.x <= 260) and (ball.x > front_check.x):
                ball.vel_a = 0
                ball.vel_d = 10

                move_right(setting)
                move_right(spike_test)
                move_right(wall_one)
                move_right(wall_two)
                move_right(front_check)
                move_right(back_check)
                move_right(floor_one)

            if (ball.x >= 260) and (ball.x <= 940):
                ball.vel_a = 10
                ball.vel_d = 10

            if (ball.x - ball.radius) <= (wall_one.x + wall_one.width):
                ball.vel_a = 0
                ball.vel_d = 10


        if keys[pygame.K_d]:

            ball.x += ball.vel_d

            if ((ball.x + ball.radius) >= 940) and ((ball.x + ball.radius) < back_check.x):
                ball.vel_a = 10
                ball.vel_d = 0

                move_left(setting)
                move_left(spike_test)
                move_left(wall_one)
                move_left(wall_two)
                move_left(front_check)
                move_left(back_check)
                move_left(floor_one)

            if (ball.x >= 260) and (ball.x <= 940):
                ball.vel_a = 10
                ball.vel_d = 10
        
        if not(ball.jump):
            if keys[pygame.K_SPACE]:
                ball.jump = True
            
        else:
            if ball.jump_count >= -7:
                ball.y -= (ball.jump_count * abs(ball.jump_count))
                ball.jump_count -= 1
            else:
                ball.jump_count = 7
                ball.jump = False



        ball.create(ball.x, ball.y)
        wall_one.create(wall_one.x, wall_one.y)
        wall_one.mask()
        wall_two.create(wall_two.x, wall_two.y)
        floor_one.create(floor_one.x, floor_one.y)
        floor_one.mask()
        spike_test.create(spike_test.x, spike_test.y)

        front_check.create(front_check.x, front_check.y)
        back_check.create(back_check.x, back_check.y)

        falling_spike_collision(spike_test, ball, player_health)
        player_health.spawn_health()


        pygame.display.update()

        # Close the game when the user clicks the "x" in the corner
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(pygame.font.get_fonts())


    pygame.quit()

print(main())