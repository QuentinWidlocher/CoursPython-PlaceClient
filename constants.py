from pygame.constants import K_1, K_2, K_3, K_4, K_5


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

GRID_SIZE = 30
CELL_SIZE = 30

COLORS = [
    WHITE,
    BLACK,
    RED,
    GREEN,
    BLUE,
    MAGENTA,
    CYAN
]

COLORS_BY_KEY = [
    None,
    None,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5
]

BASE_URL = 'http://127.0.0.1:5000/'
PLACE_URL = BASE_URL + 'place'
JSON_HEADERS = {"content-type": "application/json"}
