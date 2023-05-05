import pygame, sys

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, velocity_x, velocity_y, image_path=None):
		super().__init__()
		self.position = (x, y)
		self.velocity = (velocity_x, velocity_y)
		#self.image = pygame.image.load(image_path)

	def update(self):
		self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

	def draw(self, surface):
		pygame.draw.circle(surface, (255, 0, 0), self.position, 10)
		# surface.blit(self.image, self.position)

	def move_left(self):
		self.velocity = (-1, self.velocity[1])

	def move_right(self):
		self.velocity = (1, self.velocity[1])

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (640, 480)

# Create a window
window = pygame.display.set_mode(window_size)

# Create a player sprite
player = Player(320, 240, 0, 0)

# Main game loop
while True:
	# Handle events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.move_left()
			elif event.key == pygame.K_RIGHT:
				player.move_right()

	# Update the player sprite
	player.update()

	# Clear the window
	window.fill((255, 255, 255))

	# Draw the player sprite
	player.draw(window)

	# Update the display
	pygame.display.update()