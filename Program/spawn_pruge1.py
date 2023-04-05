import pygame


def main():
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen = pygame.display.set_mode((600, 800), 0, 32)
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button down.
                    last = (event.pos[0]-event.rel[0], event.pos[1]-event.rel[1])
                    pygame.draw.line(screen, BLACK, last, event.pos, 1)

        pygame.display.update()
        clock.tick(30)  # Limit the frame rate to 30 FPS.

if __name__ == "__main__":
    main()