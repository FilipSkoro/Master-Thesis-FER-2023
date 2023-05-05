import pygame, math, os
from pygame.locals import *

def update(player):
    if player.x <= 300 and player.x >= 100:
        player.x += 0.5
        player.y += 0.5

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (640, 480)

# Create a window
window = pygame.display.set_mode(window_size)

# Create a player sprite
player = pygame.Rect(150, 150, 20, 20)

# Clock
clock = pygame.time.Clock()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    update(player)

    # Clear the window
    window.fill((255, 255, 255))

    # Draw the player sprite
    pygame.draw.rect(window, (255, 0, 0), player)

    # Update the display
    pygame.display.update()
    clock.tick(30)