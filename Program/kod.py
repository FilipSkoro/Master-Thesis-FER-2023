import pygame
pygame.init()

win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("TopDown")
clock = pygame.time.Clock()

player_image = pygame.image.load("D:\FER_2023\Diplomski rad\Images\Custom Stop\Train_Stop.png").convert_alpha()
player_rect = player_image.get_rect(center = (350, 350), size=(200,100))
vel = 5

run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    player_rect.x += (keys[pygame.K_d] - keys[pygame.K_a]) * vel
    player_rect.y += (keys[pygame.K_s] - keys[pygame.K_w]) * vel
            
    win.fill((64, 238, 255))
    win.blit(player_image, player_rect)
    pygame.display.update()

pygame.quit()