import pygame
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE

class MainScreen:
    def __init__(self, screen):
        self.screen = screen

        #background
        self.logo = pygame.image.load(
            "assets/images/background.jpg"
        ).convert_alpha()

        self.logo_rect = self.logo.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        )

        self.bg_color = (245, 245, 245)

        #start button
        self.start_button = self.create_start_button()

    def create_start_button(self):
        normal = pygame.image.load(
            "assets/images/start_btn.jpg"
        ).convert_alpha()

        hover = pygame.image.load(
            "assets/images/start_btn_hover.jpg"
        ).convert_alpha()

        normal = pygame.transform.smoothscale(normal, BUTTON_SIZE)
        hover = pygame.transform.smoothscale(hover, BUTTON_SIZE)

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120),
            callback=self.start_game
        )

    def start_game(self):
        print("START TEST")

    def handle_event(self, event):
        self.start_button.handle_event(event)

    def update(self):
        self.start_button.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.logo, self.logo_rect)
        self.start_button.draw(self.screen)