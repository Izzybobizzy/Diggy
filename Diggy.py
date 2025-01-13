import pygame
from time import sleep

pygame.init()
pygame.font.init()

FPS = 60

#Window set up
WIN_WIDTH = 1200
WIN_HEIGHT = 700

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
NAME = pygame.display.set_caption("Diggy's Dungeon Disaster")

#All fonts
HEALTH_BAR_FONT = pygame.font.SysFont("vladimirscript", 17)

#All images and transformed images
BACKGROUND = pygame.image.load("Cave dungion.png")
wall = pygame.image.load("cave wall.png")
base_diggy = pygame.image.load("My Digging Friend.png")
OFF_DIGGY = pygame.transform.scale(base_diggy, (48, 60))
LONG_WALL = pygame.transform.scale(wall, (188, 700))

#All colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



class Player:

    def __init__(self, png, x, y ,radius, colour, vel_a, vel_d, gravity):
        self.png = png
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.vel_a = vel_a
        self.vel_d = vel_d
        self.gravity = gravity

    def create(self):
        pygame.draw.circle(WINDOW, self.colour, (self.x, self.y), self.radius)

        WINDOW.blit(self.png, (self.x - 24, self.y - 30))

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

    def back_image(self):
        WINDOW.blit(self.png, (self.x, self.y))

class Block:

    def __init__(self, png, x, y, width, height, x_vel):
        self.png = png
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_vel = x_vel

    def create(self):
        pygame.draw.rect(WINDOW, BLACK, (self.x, self.y, self. width, self.height))

        WINDOW.blit(self.png, (self.x, self.y))


class Spikes:

    def __init__(self, x, y, width, height, fall_vel, colour, x_vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fall_vel = fall_vel
        self.colour = colour
        self.x_vel = x_vel


    def create(self):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, self.width, self.height))


class CheckPoint():

    def __init__(self, x, y, radius, x_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = x_vel

    def create(self):
        pygame.draw.circle(WINDOW, RED, (self.x, self.y), self.radius)

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
    ball = Player(OFF_DIGGY, 600, 600, 18, WHITE, 10, 10, 1)

    #Background of game
    setting = Background(BACKGROUND, 0, 0, 10)

    #Left wall at begining
    wall_one = Block(LONG_WALL, 0, 0, 188, 700, 10)

    #Second wall that placed before the left wall
    wall_two = Block(LONG_WALL, -188, 0, 188, 700, 10)

    #temporary spike
    spike_test = Spikes(800,0, 10, 80, 25, BLACK, 10)

    #Players health bar
    player_health = HealthBar(100)

    #Check point to start objects from moving at the start
    front_check = CheckPoint(250, 600, 10, 10)

    #Check point to start objects from moving at the end
    back_check = CheckPoint(3550, 600, 10, 10)

    run = True

    while run:

        clock.tick(FPS)

        pygame.time.delay(50)

        setting.back_image()

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

            if (ball.x >= 260) and (ball.x <= 940):
                ball.vel_a = 10
                ball.vel_d = 10



        ball.create()
        wall_one.create()
        wall_two.create()
        spike_test.create()

        front_check.create()
        back_check.create()

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