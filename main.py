import requests
from game import Game
from constants import  CELL_SIZE, COLORS, GRID_SIZE, WHITE
import pygame
from pygame import display
from pygame import event

def main():
    pygame.init()
    screen = display.set_mode((CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE))

    # On commence avec un écran de la couleur par défaut (blanc)
    screen.fill(COLORS[0])

    running = False

    # On ne lance le jeu que si le serveur est joignable
    try:
        game = Game(screen)
        running = True
    except requests.exceptions.ConnectionError:
        print('Impossible de joindre le serveur, veuillez relancer le jeu')

    while running:
        # event.pump() permet de dire à PyGame de gérer les évènements
        event.pump()

        # Dans ce projet, on n'efface pas l'écran à chaque frame du coup

        game.update()
        display.update()

if __name__ == '__main__':
    main()
