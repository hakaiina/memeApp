import pygame
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE


class RegisterScreen:
    def __init__(self, screen, db, switch_screen_callback):
        self.screen = screen
        self.db = db
        self.switch_screen = switch_screen_callback

        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"
        self.font_text = pygame.font.Font(font_path, 48)

        self.bg_color = (245, 245, 245)

        # input fields
        self.username = ""
        self.password = ""

        self.active_input = "username"

        # register button
        self.register_btn = self.create_button()


    def create_button(self):
        normal = pygame.Surface(BUTTON_SIZE)
        normal.fill((100, 200, 100))

        hover = pygame.Surface(BUTTON_SIZE)
        hover.fill((80, 180, 80))

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150),
            callback=self.register_user
        )


    def register_user(self):
        if self.username and self.password:
            self.db.add_user(self.username, self.password)

            # transition to the test
            from screens.main_screen import MainScreen
            self.switch_screen(MainScreen(self.screen))


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # switch fields
                self.active_input = (
                    "password" if self.active_input == "username" else "username"
                )
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == "username":
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            else:
                if self.active_input == "username":
                    self.username += event.unicode
                else:
                    self.password += event.unicode

        self.register_btn.handle_event(event)


    def update(self):
        self.register_btn.update()


    def draw(self):
        self.screen.fill(self.bg_color)

        title = self.font_text.render("Регистрация", True, (0, 0, 0))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 100, 100))

        username_text = self.font_text.render(
            f"Имя: {self.username}",
            True,
            (0, 0, 0)
        )

        password_hidden = "*" * len(self.password)
        password_text = self.font_text.render(
            f"Пароль: {password_hidden}",
            True,
            (0, 0, 0)
        )

        self.screen.blit(username_text, (SCREEN_WIDTH // 2 - 200, 250))
        self.screen.blit(password_text, (SCREEN_WIDTH // 2 - 200, 320))

        self.register_btn.draw(self.screen)