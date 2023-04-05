import pygame
from pygame.locals import *

### General parameters ###
# window parameters
win_width = 600
win_height = 600
win_color = (255, 255, 255) # white

# pygame and window init
pygame.init()
pygame.display.set_caption("Spawn pruge")
window = pygame.display.set_mode((win_width, win_height))
window.fill(win_color)

# line lists
line_coordinates = []

### Main loop ###
run = True
while run:

    # iterating over all the events received from pygame.event.get()
    for event in pygame.event.get():

        if event.type == QUIT:
            run = False

        elif event.type == MOUSEBUTTONDOWN:
            # saving coordinates on which LEFT mouse button clicked
            line_coordinates.append(event.pos)

            if len(line_coordinates) >= 2:
                # line color and width
                line_color = (0, 0, 0) # black
                line_width = 3
                # line coordinates
                start_pos = (line_coordinates[len(line_coordinates)-2][0], line_coordinates[len(line_coordinates)-2][1])
                end_pos = (line_coordinates[len(line_coordinates)-1][0], line_coordinates[len(line_coordinates)-1][1])
                # create rectangle
                pygame.draw.line(window, line_color, start_pos, end_pos, line_width)             

            else:
                pass

    # draws the surface object to the screen
    pygame.display.update()

pygame.quit