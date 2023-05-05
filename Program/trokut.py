import pygame
pygame.init()

screen = pygame.display.set_mode([500, 500])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.draw.polygon(screen, (0, 255, 255), ((125,125),(125,150),(150,125+25/2)))

    pygame.display.flip()

pygame.quit()