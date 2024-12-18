
##################
###PREGAME CODE###
##################

#imports and initializations
import pygame 
from time import sleep

import pygame.gfxdraw
pygame.init() 
pygame.mixer.init()
pygame.font.init()


#window display setup 
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("This is Diggy dummie :D") 


#Loads Assets
BACKGROUND_1 = pygame.image.load("img_assets/cave.png")
BACKGROUND_2 = pygame.image.load("img_assets/Dark_corners.png")
UI_1 = pygame.image.load("img_assets/healthbar.png")
PLAYER_1 = pygame.image.load("img_assets/idle_1.png")
WALKING_SND = pygame.mixer.Sound("snd_assets/player_footsteps.mp3")
FONT_1 = pygame.font.Font("img_assets/ElixiR.ttf", 25)

#Colour Constants
GOLD = (255, 215, 0)
RED = (124, 10, 2)



#Resize images and backgrounds / stores them
PLAYER_WIDTH = 75
PLAYER_HEIGHT = 100
OBJECT_WIDTH = 100
OBJECT_HEIGHT = 100
HEALTHBAR_SIZE = (250,50)
BACKGROUND_WIDTH = WINDOW_WIDTH*2
BACKGROUND_HEIGHT = WINDOW_HEIGHT

sprite = pygame.transform.scale(PLAYER_1, (PLAYER_WIDTH,PLAYER_HEIGHT))
cave = pygame.transform.scale(BACKGROUND_1, (BACKGROUND_WIDTH,BACKGROUND_HEIGHT))
healthbar = pygame.transform.scale(UI_1, HEALTHBAR_SIZE)
overlay = pygame.transform.scale(BACKGROUND_2, (BACKGROUND_WIDTH,BACKGROUND_HEIGHT))



#Classes
class Objects:

    VELOCITY = 20

    def __init__(self, image, health, x, y,):
        self.image = image
        self.health = health
        self.x = x
        self.y = y
     
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


def ball_collision_check(player, object): 
   # check for collision with right side of a object 
    if (player.x - PLAYER_WIDTH) <= (object.x + PLAYER_WIDTH) and (player.y >= object.y) and (player.y <= object.y + PLAYER_HEIGHT): 
        player.health -= 25

    # check for collision with right side of a object
    if (player.x + PLAYER_WIDTH) >= object.x and (player.x + PLAYER_WIDTH) <= (object.x + OBJECT_WIDTH) and (player.y >= object.y) and (player.y <= object.y + OBJECT_HEIGHT):
        player.health -=25




#music playlist loop: loads and plays them infinitely
playlist = ["snd_assets/Habanera.mp3"]
while not pygame.mixer.music.get_busy():
    played = playlist.pop(0)
    playlist.append(played)
    pygame.mixer.music.load(playlist[-1])
    pygame.mixer.music.play(1,0,1)




###############
###GAME CODE###
###############

def main(): 

    #Creates assets
    player_1 = Objects(sprite, 100, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    player_health = FONT_1.render(f"Health: {player_1.health}", True, GOLD)
    background = Objects(cave, 100, 0, 0)



    #run until user closes the display window 
    closed = False 
    while not closed:

        pygame.time.delay(30)

        #Makes the assets on the window
        Objects.draw(background,WINDOW)
        Objects.draw(player_1,WINDOW)
        WINDOW.blit(overlay,(0,0))


        pygame.gfxdraw.box(WINDOW,(60,48,220,25),RED)
        WINDOW.blit(healthbar,(35,35))
        WINDOW.blit(player_health,(40,10))

        #Checks for player collision with object
        ####


        #loop through possible keyboard and mouse events 
        for event in pygame.event.get():


            #if user clicks on close button (X) in top R corner -> close window 
            if event.type == pygame.QUIT: 
                closed = True 
                break
            #Allows the user to move and give input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and BACKGROUND_WIDTH >= WINDOW_WIDTH +1:
                background.x += Objects.VELOCITY           
            if keys[pygame.K_d] and BACKGROUND_WIDTH >= 1:
                background.x -= Objects.VELOCITY
            if keys[pygame.K_SPACE]:
                background.y += Objects.VELOCITY

                

        #Updates what the window shows
        pygame.display.update()

    #user is done -> terminate program 
    pygame.quit() 
 
#call main method 
if __name__ == "__main__": 
    main()