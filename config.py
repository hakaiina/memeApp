import os

#window settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60

#button
BUTTON_SIZE = (280, 100)

#db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db/memeApp.db")