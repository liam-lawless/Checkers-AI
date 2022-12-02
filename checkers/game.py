# Handles game properties
# i.e. Whos turn it is, can a piece move to a certain tile, has a player selected a piece

import pygame
from .constant_variables import RED, BLACK, GREEN, SIZE
from .board import Board

class Game:

    def __init__(self, window):
        self._init()
        self.window = window

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()
        
    # Determines whether on not a piece should move based on what has been selected
    def select(self, row, col):
        # Attempt to select a piece on the board
        if self.selected:
            result = self._move(row, col)
            # If fails, remove the current selection and reselect a new piece
            if not result:
                self.selected = None
                self.select(row, col) 

        piece = self.board.get_piece(row, col)
        # Not an empty tile, selecting a valid piece
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        # if the user has selected a valid piece and the tile to move to is empty and is a valid move
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # move the currently selected piece to the row and column that the user selects
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row,col)]
            # Remove a piece if it was jumped
            if skipped:
                self.board.remove(skipped)
            # Change the turn to the other player
            self.change_turn()
            
        else:
            return False
        
        return True

    # Change the turn 
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = BLACK
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, (col * SIZE + SIZE // 2, row * SIZE + SIZE // 2), 15)

    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()