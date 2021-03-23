from constants import CELL_SIZE, COLORS, COLORS_BY_KEY, FULL_BOARD_URL, GRID_SIZE, JSON_HEADERS, PLACE_URL, WHITE
import math
from pygame import Surface, key, mouse
from json import dumps as stringify
import requests

class Game:

    def __init__(self, screen: Surface):
        # On garde la référence de l'écran pour faciliter le code
        self.screen = screen

        # On retient l'état des clic de la souris, pour éviter de 
        # recliquer si le bouton n'est pas relaché avant
        self.l_mouse_pressed = False
        self.r_mouse_pressed = False

        # Timer qui augmente à chaque frame, pour temporiser le refresh
        self.time_before_fetch = 0

        # On récupère l'état du canvas dès le début
        self.fetch_server()

    def update(self):
    
        if mouse.get_pressed()[0]:
            # Si le bouton gauche de la souris est enfoncé...
            if not self.l_mouse_pressed:
                # ... et que l'on n'était pas déjà en train de l'enfoncer,
                self.l_mouse_pressed = True
                # On déclenche le clic
                self.on_l_mouse_click()
        else:
            # Si le bouton est relaché on le retient
            self.l_mouse_pressed = False

        # Idem pour le bouton droit de la souris
        if mouse.get_pressed()[2]:
            if not self.r_mouse_pressed:
                self.r_mouse_pressed = True
                self.on_r_mouse_click()
        else:
            self.r_mouse_pressed = False

        # On incrémente le compteur avant le refresh
        self.time_before_fetch += 1

        # Si le compteur arrive à un certain point, on récupère
        # les infos du serveur et on remet le compteur à 0
        if self.time_before_fetch >= 2000:
            self.fetch_server()
            self.time_before_fetch = 0

    def on_l_mouse_click(self):
        # Par défaut on prend la couleur 1, le noir
        color = 1
        
        # On parcours les couleurs par index
        for i in range(len(COLORS_BY_KEY)):
            # On récupère la touche de la boucle
            k = COLORS_BY_KEY[i]

            # Si cette touche est enfoncée, on retient la couleur 
            if k and key.get_pressed()[k]:
                color = i

        self.on_mouse_click(color)

    def on_r_mouse_click(self):
        self.on_mouse_click(0)

    def on_mouse_click(self, color):
        # On récupère la position de la souris, entre 0 et GRID_SIZE*100
        pos = mouse.get_pos()

        # Pour convertir cette taille en grille de CELL_SIZE par CELL_SIZE,
        # On divise et on arrondi à l'inférieur le x et le y
        (x, y) = (math.floor(pos[0] / CELL_SIZE),
                math.floor(pos[1] / CELL_SIZE))

        # On trace le pixel à l'écran et on indique ça au serveur
        self.draw_pixel(x, y, color)
        self.inform_server(x, y, color)

    def draw_pixel(self, x, y, color):
        # Chaque cellule est composé de CELL_SIZE carré de pixel.
        # On boucle du cette quantité et on rempli la cellule de pixels 
        for i in range(CELL_SIZE):
            for j in range(CELL_SIZE):
                self.screen.set_at((x*CELL_SIZE+i, y*CELL_SIZE+j), COLORS[color])

    def inform_server(self, x, y, color):
        # On forme l'objet que l'on va envoyer au serveur
        body = {
            "x": x,
            "y": y,
            "color": color
        }

        # On effectue une requête POST avec ces info et on indique au serveur
        # qu'il s'agit de données format JSON
        requests.post(PLACE_URL, stringify(body), headers=JSON_HEADERS)

    def fetch_server(self):
        # On récupère la grille depuis le serveur
        grid = requests.get(FULL_BOARD_URL).json()

        # On efface l'écran
        self.screen.fill(WHITE)

        # Pour chaque pixel, on le dessine à l'écran comme ferais un clic
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = grid[x][y]
                self.draw_pixel(x, y, color)

        
