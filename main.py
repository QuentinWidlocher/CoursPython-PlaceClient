import socketio
from game import Game
from constants import  CELL_SIZE, GRID_SIZE, PLACE_URL, WHITE
import pygame
from pygame import display
from pygame import event

def main():
    pygame.init()
    screen = display.set_mode((CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE))
    screen.fill(WHITE)

    running = False

    try:
        game = Game(screen)
        running = True
    except socketio.exceptions.ConnectionError:
        print('Impossible de joindre le serveur, veuillez relancer le jeu')

    while running:
        event.pump()
        game.update()
        display.update()

if __name__ == '__main__':
    main()
