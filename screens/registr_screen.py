import pygame
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE_REGISTER


class RegisterScreen:
    def __init__(self, screen, db, switch_screen_callback):
        self.screen = screen

        self.background = pygame.image.load("assets/images/bg_register.jpg").convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.db = db
        self.switch_screen = switch_screen_callback

        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"
        self.font_text = pygame.font.Font(font_path, 58)
        self.font_text_btn = pygame.font.Font(font_path, 28)
        self.font_fields = pygame.font.Font(font_path, 46)

        self.bg_color = (245, 245, 245)

        # input fields
        self.username = ""
        self.password = ""

        self.active_input = None

        # placeholder
        self.username_placeholder = "Введите имя"
        self.password_placeholder = "Введите пароль"

        # cursor
        self.cursor_visible = True
        self.cursor_timer = 0


        self.username_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 200,
            260,
            400,
            60
        )

        self.password_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 200,
            350,
            400,
            60
        )

        #colors fields
        self.input_color = (255, 255, 255)
        self.active_color = (220, 240, 255)
        self.border_color = (0, 0, 0)
        self.placeholder_color = (150, 150, 150)

        # register button
        self.register_btn = self.create_button()


    def create_button(self):
        normal = pygame.Surface(BUTTON_SIZE_REGISTER)
        normal.fill((120, 200, 120))

        hover = pygame.Surface(BUTTON_SIZE_REGISTER)
        hover.fill((100, 180, 100))

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200),
            callback=self.register_user
        )


    def register_user(self):
        if self.username and self.password:
            self.db.add_user(self.username, self.password)

            # transition to the test
            from screens.main_screen import MainScreen
            self.switch_screen(MainScreen(self.screen))


    def handle_event(self, event):
        # select field by click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.username_rect.collidepoint(event.pos):
                self.active_input = "username"
            elif self.password_rect.collidepoint(event.pos):
                self.active_input = "password"
            else:
                self.active_input = None

        # input text
        if event.type == pygame.KEYDOWN and self.active_input:

            if event.key == pygame.K_BACKSPACE:

                if self.active_input == "username":
                    self.username = self.username[:-1]

                if self.active_input == "password":
                    self.password = self.password[:-1]

            else:

                if self.active_input == "username":
                    self.username += event.unicode

                if self.active_input == "password":
                    self.password += event.unicode

        self.register_btn.handle_event(event)


    def update(self):
        self.register_btn.update()

        self.cursor_timer += 1

        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0


    def draw(self):

        self.screen.blit(self.background, (0, 0))

        title = self.font_text.render("Регистрация", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # username field
        color = self.active_color if self.active_input == "username" else self.input_color

        pygame.draw.rect(self.screen, color, self.username_rect)
        pygame.draw.rect(self.screen, self.border_color, self.username_rect, 2)

        username_text = self.username

        if self.active_input == "username" and self.cursor_visible:
            username_text += "|"

        if self.username == "" and self.active_input != "username":
            surface = self.font_fields.render(
                self.username_placeholder,
                True,
                self.placeholder_color
            )
        else:
            surface = self.font_fields.render(
                username_text,
                True,
                (0, 0, 0)
            )
        rect = surface.get_rect(
            midleft=(self.username_rect.x + 10, self.username_rect.centery - 5)
        )

        self.screen.blit(surface, rect)

        # password field
        color = self.active_color if self.active_input == "password" else self.input_color

        pygame.draw.rect(self.screen, color, self.password_rect)
        pygame.draw.rect(self.screen, self.border_color, self.password_rect, 2)

        hidden_password = "*" * len(self.password)

        if self.active_input == "password" and self.cursor_visible:
            hidden_password += "|"

        if self.password == "" and self.active_input != "password":

            surface = self.font_fields.render(
                self.password_placeholder,
                True,
                self.placeholder_color
            )
        else:
            surface = self.font_fields.render(
                hidden_password,
                True,
                (0, 0, 0)
            )

        rect = surface.get_rect(
            midleft=(self.password_rect.x + 10, self.password_rect.centery - 5)
        )
        self.screen.blit(surface, rect)

        # button
        self.register_btn.draw(self.screen)

        btn_text = self.font_text_btn.render(
            "Зарегистрироваться",
            True,
            (0, 0, 0)
        )
        btn_rect = btn_text.get_rect(
            center=self.register_btn.rect.center
        )
        self.screen.blit(btn_text, btn_rect)