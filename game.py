from pygame.constants import K_1, K_2
from constants import BASE_URL, CELL_SIZE, COLORS, COLORS_BY_KEY, WHITE
import math
from pygame import key, mouse
from json import dumps as stringify
import socketio

class Game:

    io = socketio.Client()

    def __init__(self, screen):
        self.screen = screen
        self.l_mouse_pressed = False
        self.r_mouse_pressed = False
        self.io.connect(BASE_URL)
        self.io.on('place', self.on_io_update)

    def update(self):
        if mouse.get_pressed()[0]:
            if not self.l_mouse_pressed:
                self.l_mouse_pressed = True
                self.on_l_mouse_click()
        else:
            self.l_mouse_pressed = False

        if mouse.get_pressed()[2]:
            if not self.r_mouse_pressed:
                self.r_mouse_pressed = True
                self.on_r_mouse_click()
        else:
            self.r_mouse_pressed = False

    def on_l_mouse_click(self):
        color = 1
        
        for i in range(len(COLORS_BY_KEY)):
            k = COLORS_BY_KEY[i]
            if k and key.get_pressed()[k]:
                color = i

        self.on_mouse_click(color)

    def on_r_mouse_click(self):
        self.on_mouse_click(0)

    def on_mouse_click(self, color):
        pos = mouse.get_pos()
        (x, y) = (math.floor(pos[0] / CELL_SIZE),
                math.floor(pos[1] / CELL_SIZE))
        self.inform_server(x, y, color)
        self.draw_pixel(x, y, color)

    def draw_pixel(self, x, y, color):
        for i in range(CELL_SIZE):
            for j in range(CELL_SIZE):
                self.screen.set_at((x*CELL_SIZE+i, y*CELL_SIZE+j), COLORS[color])


    def inform_server(self, x, y, color):
        body = {}
        body['x'] = x
        body['y'] = y
        body['color'] = color
        self.io.emit('place', stringify(body))

    def on_io_update(self, data):
        self.draw_pixel(data['x'], data['y'], data['color'])
        
