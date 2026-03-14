import os

#window settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60

PADDING = 20
BUTTON_WIDTH = 600
BUTTON_HEIGHT = 80
NAV_BUTTON_WIDTH = 150
NAV_BUTTON_HEIGHT = 50

#button
BUTTON_SIZE_REGISTER = (280, 80)
BUTTON_SIZE = (280, 100)

#db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db/memeApp.db")