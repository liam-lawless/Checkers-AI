# Contains our board class that represents our checkers board
# handles pieces moving, deleting pieces, drawing pieces onto the screen
import pygame
from .constant_variables import *
from .piece import Piece


class Board:

    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.init_board()

    # Draws the tiles for our checkerboard
    def draw_tiles(self, window):
        # set the background as black
        window.fill(BLACK)

        # draw tiles for rows and columns
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, WHITE, (row*SIZE, col*SIZE, SIZE, SIZE))

    def move(self, piece, row, col):
        # Swap variables
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0 and not piece.is_king():
            piece.king_me()

            if piece.color == RED:
                self.red_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def init_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_tiles(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def remove(self, pieces):
        for piece in pieces:
             self.board[piece.row][piece.col] = 0

             if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return RED

        return None

    def get_valid_moves(self, piece):
        # store the move as a key
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min (row + 3, ROWS), 1, piece.color, right))

        return moves


    #Returns all of the valid moves for a given piece
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):
            # if the left tile is outside of the board
            if left < 0:
                break

            current = self.board[r][left]
            # 
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,left)] = last + skipped
                else:
                    moves[(r,left)] = last

                # skipped over a piece, checking if we can jump consecutively
                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + r, ROWS)
                    
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped = last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped = last))
                break
            #
            elif current.color == color:
                break
            # otherwise its not the players color so it mus be the oppenents color
            else:
                last = [current]

            left -= 1

        return moves

    # Returns all of the valid moves for a given piece
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []

        for r in range(start, stop, step):
            # if the left tile is outside of the board
            if right >= COLS:
                break

            current = self.board[r][right]
            # 
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r,right)] = last

                # skipped over a piece, checking if we can jump consecutively
                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + r, ROWS)
                    
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped = last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped = last))
                break
            #
            elif current.color == color:
                break
            # otherwise its not the players color so it mus be the oppenents color
            else:
                last = [current]

            right += 1

        return moves 

    def evaluate(self):
        return self.black_left - self.red_left + (self.black_kings * 0.5 - self.red_kings * 0.5)
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
                    
        return pieces