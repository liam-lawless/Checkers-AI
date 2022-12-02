# Represents a checkers piece
import pygame
from .constant_variables import RED, GRAY, SIZE, CROWN

class Piece:

    # Defines the padding for a piece on its tile
    PAD = 15
    # Defines the thickness of the outline around every piece
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.get_pos()

    # Gets the position of any piece
    def get_pos(self):
        self.x = SIZE * self.col + SIZE // 2
        self.y = SIZE * self.row + SIZE // 2

    # Turns a checkered piece into a king
    def king_me(self):
        self.king = True

    def is_king(self):
        return self.king

    def draw(self, window):
        # size of every piece
        radius = SIZE // 2 - self.PAD
        pygame.draw.circle(window, GRAY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col

        # Update the current position of the piece
        self.get_pos()
        

    def __repr__(self):
        return str(self.color)