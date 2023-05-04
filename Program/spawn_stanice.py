import pygame
from pygame.locals import *

### General parameters ###
# window parameters
win_width = 600
win_height = 600
win_color = (255, 255, 255) # white

# pygame and window init
pygame.init()
pygame.display.set_caption("Spawn stanice")
window = pygame.display.set_mode((win_width, win_height))
window.fill(win_color)

# rectangle lists
rectangles_coordinates = []

### Main loop ###
run = True
while run:

    # iterating over all the events received from pygame.event.get()
    for event in pygame.event.get():

        if event.type == QUIT:
            run = False

        elif event.type == MOUSEBUTTONDOWN:
            # saving coordinates on which LEFT mouse button clicked
            position = event.pos
            rectangles_coordinates.append(position)

            ## Creating rectangle ##
            # rectangle color, width and height
            rect_color = (0, 0, 0) # black
            rect_width = 60
            rect_height = 30
            # rectangle coordinates
            co_x = position[0]-rect_width/2
            co_y = position[1]-rect_height/2
            # create rectangle
            pygame.draw.rect(window, rect_color, pygame.Rect((co_x, co_y), (rect_width, rect_height)))

    # draws the surface object to the screen
    pygame.display.update()

pygame.quit