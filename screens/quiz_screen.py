import pygame
import json
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class QuizScreen:
    def __init__(self, screen, db, switch_screen, username):
        self.screen = screen
        self.switch_screen = switch_screen

        # for saving user progress
        self.db = db
        self.username = username

        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"

        self.title_font = pygame.font.Font(font_path, 28)
        self.text_font = pygame.font.Font(font_path, 14)

        # background
        self.logo = pygame.image.load(
            "assets/images/backgr.jpg"
        ).convert_alpha()

        self.logo_rect = self.logo.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        )

        self.bg_color = (245, 245, 245)

        # load questions
        self.questions = self.load_questions()

        self.current_question = 0
        self.score = 0

        # selected answer
        self.selected_answer = None

        # text input
        self.active_input = False
        self.user_text = ""

        # buttons
        self.answer_btns = []
        self.create_answer_buttons()

        self.submit_button = self.create_submit_button()
        self.menu_button = self.create_menu_button()


    @staticmethod
    def load_questions():
        with open("db/questions.json", "r", encoding="utf-8") as file:
            return json.load(file)


    def create_answer_buttons(self):
        for i in range(4):
            normal = pygame.Surface((400, 40))
            normal.fill((200, 200, 255))

            hover = pygame.Surface((400, 40))
            hover.fill((170, 170, 240))

            button = Button(
                image=normal,
                hover_image=hover,
                pos=(SCREEN_WIDTH // 2, 200 + i * 30),
                callback=lambda idx=i: self.select_answer(idx)
            )
            self.answer_btns.append(button)


    def create_submit_button(self):
        normal = pygame.Surface((200, 60))
        normal.fill((120, 200, 120))

        hover = pygame.Surface((200, 60))
        hover.fill((100, 180, 100))

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2 -  310, SCREEN_HEIGHT - 80),
            callback=self.submit_answer
        )


    def create_menu_button(self):
        normal = pygame.Surface((200, 60))
        normal.fill((200, 120, 120))

        hover = pygame.Surface((200, 60))
        hover.fill((180, 100, 100))

        from screens.main_screen import MainScreen

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2 + 310, SCREEN_HEIGHT - 80),
            callback=lambda: self.switch_screen(MainScreen(self.screen, self.db, self.switch_screen, self.username))
        )


    def select_answer(self, index):
        self.selected_answer = index


    def submit_answer(self):
        question = self.questions[self.current_question]

        # choice answer
        if question["type"] == "choice":
            if self.selected_answer is None:
                return
            if self.selected_answer == question["correct"]:
                self.score += 2

        # text answer
        if question["type"] == "text":
            user_answer = self.user_text.lower().strip()

            if user_answer in question["answer"]:
                self.score += 3
            self.user_text = ""

        self.selected_answer = None
        self.current_question += 1

        # end test
        if self.current_question >= len(self.questions):
            print("END TEST")
            print("Score: ", self.score)


    def handle_event(self, event):
        question = self.questions[self.current_question]

        if question["type"] == "choice":
            for button in self.answer_btns:
                button.handle_event(event)

        if question["type"] == "text":
            # select field by click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active_input = True
                else:
                    self.active_input = False

            if event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode

        self.submit_button.handle_event(event)
        self.menu_button.handle_event(event)


    def update(self):
        for button in self.answer_btns:
            button.update()

        self.submit_button.update()
        self.menu_button.update()


    def draw(self):
        self.screen.fill(self.bg_color)

        question = self.questions[self.current_question]

        # question text
        question_text = self.render_text(
            text=question["text"],
            font=self.title_font,
            color=(0, 0, 0),
            max_width=SCREEN_WIDTH - 80,
            line_spacing=1
        )
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(question_text, question_rect)

        # image
        image_y = question_rect.bottom + 10 # margin for image

        image = pygame.image.load(question["image"]).convert_alpha()
        image = pygame.transform.scale(image, (400, 250))

        image_rect = image.get_rect(center=(SCREEN_WIDTH // 2, image_y + 125))
        self.screen.blit(image, image_rect)

        # CHOICE ANSWER
        if question["type"] == "choice":
            buttons_y = image_rect.bottom + 20 # margin for buttons

            for i, button in enumerate(self.answer_btns):
                original_y = button.rect.y
                button.rect.y = buttons_y + i * 50

                button.draw(self.screen)

                self.draw_text_in_button(
                    text=question["answers"][i],
                    font=self.text_font,
                    color=(0, 0, 0),
                    button=button
                )

                button.rect.y = original_y


        # TEXT ANSWER
        if question["type"] == "text":
            self.input_box = pygame.Rect(
                SCREEN_WIDTH // 2 - 200,
                image_rect.bottom + 50,
                400,
                60
            )
            pygame.draw.rect(self.screen, (200, 200, 200), self.input_box)

            self.draw_wrapped_text(
                text=self.user_text,
                font=self.title_font,
                color=(0, 0, 0),
                rect=self.input_box.inflate(-20, -10)
            )

        # buttons
        self.submit_button.draw(self.screen)
        self.menu_button.draw(self.screen)

    @staticmethod
    def render_text(text, font, color, max_width, line_spacing=1):
        """positioning of the text with wrap"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    chars = []
                    for char in word:
                        chars.append(char)
                        test_word = ''.join(chars)
                        if font.render(test_word, True, color).get_width() > max_width:
                            chars.pop()
                            if chars:
                                lines.append(''.join(chars))
                            chars = [char]
                    if chars:
                        current_line = [''.join(chars)]

        if current_line:
            lines.append(' '.join(current_line))

        line_heights = [font.render(line, True, color).get_height() for line in lines]
        total_height = sum(line_heights) + line_spacing * (len(lines) - 1)

        text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))

        y = 0
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            line_rect = line_surface.get_rect()

            line_rect.centerx = max_width // 2
            line_rect.y = y

            text_surface.blit(line_surface, line_rect)
            y += line_heights[i] + line_spacing

        return text_surface


    def draw_text_in_button(self, text, font, color, button):
        text_surface = self.render_text(
            text=text,
            font=font,
            color=color,
            max_width=button.rect.width - 20,
            line_spacing=3
        )

        text_rect = text_surface.get_rect(center=button.rect.center)
        self.screen.blit(text_surface, text_rect)


    def draw_wrapped_text(self, text, font, color, rect):
        text_surface = self.render_text(
            text=text,
            font=font,
            color=color,
            max_width=rect.width,
            line_spacing=5
        )

        text_rect = text_surface.get_rect()
        text_rect.x = rect.x
        text_rect.centery = rect.centery

        self.screen.blit(text_surface, text_rect)


