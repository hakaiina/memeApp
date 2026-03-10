import pygame
from ui.button import Button
from screens.quiz_screen import QuizScreen
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE


class MainScreen:
    def __init__(self, screen, db, switch_screen, username):
        self.screen = screen

        self.db = db
        self.username = username

        self.switch_screen = switch_screen

        # fonts
        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"

        self.title_font = pygame.font.Font(font_path, 64)
        self.subtitle_font = pygame.font.Font(font_path, 48)
        self.user_font = pygame.font.Font(font_path, 24)

        # background
        self.logo = pygame.image.load(
            "assets/images/backgr.jpg"
        ).convert_alpha()

        self.logo_rect = self.logo.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        )

        self.bg_color = (245, 245, 245)

        # title text surfaces
        self.title_surface = self.title_font.render(
            "Добро пожаловать!",
            True,
            (124, 17, 17)
        )

        self.subtitle_surface = self.subtitle_font.render(
            "МЕМОГРАФИЯ: ГИА ПО МЕМАМ",
            True,
            (0, 0, 0)
        )

        # text positions
        self.title_rect = self.title_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 110)
        )

        self.subtitle_rect = self.subtitle_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 195)
        )

        # user info
        self.create_user_info()

        # start button
        self.start_button = self.create_start_button()


    def create_user_info(self):
        if self.username:
            self.user_name_surface = self.user_font.render(
                f"Игрок: {self.username}",
                True,
                (50, 50, 150)
            )

            self.user_name_rect = self.user_name_surface.get_rect(
                topright=(SCREEN_WIDTH - 20, 20)
            )

            best_score = self.db.get_user_score(self.username)
            self.user_score_surface = self.user_font.render(
                f"Рекорд: {best_score}",
                True,
                (50, 50, 150)
            )

            self.user_score_rect = self.user_score_surface.get_rect(
                topright=(SCREEN_WIDTH - 20, 50)
            )
        else:
            self.user_name_surface = self.user_font.render(
                "Игрок: Гость",
                True,
                (50, 50, 150)
            )
            self.user_name_rect = self.user_name_surface.get_rect(
                topright=(SCREEN_WIDTH - 20, 20)
            )

    def create_start_button(self):
        normal = pygame.image.load(
            "assets/images/start_btn.png"
        ).convert_alpha()

        hover = pygame.image.load(
            "assets/images/start_btn_hover.png"
        ).convert_alpha()

        normal = pygame.transform.smoothscale(normal, BUTTON_SIZE)
        hover = pygame.transform.smoothscale(hover, BUTTON_SIZE)

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
            callback=self.start_game
        )

    def start_game(self):
        from screens.quiz_screen import QuizScreen
        self.switch_screen(QuizScreen(self.screen, self.db, self.switch_screen, self.username))
        print("START GAME")

    def handle_event(self, event):
        self.start_button.handle_event(event)

    def update(self):
        self.start_button.update()

    def draw(self):
        self.screen.fill(self.bg_color)

        self.screen.blit(self.logo, self.logo_rect)
        self.screen.blit(self.title_surface, self.title_rect)
        self.screen.blit(self.subtitle_surface, self.subtitle_rect)

        if hasattr(self, 'user_name_surface'):
            self.screen.blit(self.user_name_surface, self.user_name_rect)
            if hasattr(self, 'user_score_surface'):
                self.screen.blit(self.user_score_surface, self.user_score_rect)

        self.start_button.draw(self.screen)