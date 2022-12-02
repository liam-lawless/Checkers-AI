# Contains all of our constant variables that will be used across the project
import pygame

# Size of the board
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SIZE = WIDTH // COLS

# Colors for the board (RGB)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44,25))

DRAW = True