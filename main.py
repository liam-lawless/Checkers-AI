import pygame
from checkers.constant_variables import WIDTH, HEIGHT, SIZE, BLACK
from checkers.game import Game
from minimax.algorithm import minimax

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Speed of our game
FPS = 60

# Returns the row and column that the mouse is currently in
def get_mouse_pos(pos):
    x, y = pos
    row = y // SIZE
    col = x // SIZE

    return row, col

def main():
    # event loop that runs X times per second
    run = True
    # determines the running speed (at max) of the program
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    ai_depth = 2

    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            value, new_board = minimax(game.get_board(), ai_depth, BLACK, game)
            game.ai_move(new_board)
            

        if game.winner() != None:
            print(game.winner())
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                
                game.select(row, col)

        
            
        game.update()
        
    pygame.quit()

main()