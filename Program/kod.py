import pygame

def get_line(x1, y1, x2, y2):
    """Funkcija koja vraća sve točke na liniji između dvije točke."""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    x = x1
    y = y1
    points = []
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    points.append((x, y))
    return points

# Primjer korištenja
pygame.init()

screen = pygame.display.set_mode((640, 480))

points = get_line(0, 0, 320, 240)

print(points)

for point in points:
    pygame.draw.circle(screen, (255, 0, 0), point, 3)

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
