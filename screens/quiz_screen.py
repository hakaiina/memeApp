import pygame
import json
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class QuizScreen:
    def __init__(self, screen, switch_screen):
        self.screen = screen
        self.switch_screen = switch_screen

        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"

        self.title_font = pygame.font.Font(font_path, 60)
        self.text_font = pygame.font.Font(font_path, 40)

        self.bg_color = (255, 255, 255)

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


    def load_questions(self):
        with open("db/questions.json", "r", encoding="utf-8") as file:
            return json.load(file)


    def create_answer_buttons(self):
        for i in range(4):
            normal = pygame.Surface((500, 60))
            normal.fill((200, 200, 255))

            hover = pygame.Surface((500, 60))
            hover.fill((170, 170, 240))

            button = Button(
                image=normal,
                hover_image=hover,
                pos=(SCREEN_WIDTH // 2, 400 + i * 80),
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
            pos=(SCREEN_WIDTH // 2 -  150, SCREEN_HEIGHT - 80),
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
            pos=(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT - 80),
            callback=lambda: self.switch_screen(MainScreen(self.screen))
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
        text_surface = self.title_font.render(
            question["text"],
            True,
            (0, 0, 0)
        )
        rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(text_surface, rect)

        # image
        image = pygame.image.load(question["image"]).convert_alpha()
        image = pygame.transform.scale(image, (400, 250))

        image_rect = image.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(image, image_rect)

        # CHOICE ANSWER
        if question["type"] == "choice":
            for i, button in enumerate(self.answer_btns):
                button.draw(self.screen)
                text = self.font.render(
                    question["answer"][i],
                    True,
                    (0, 0, 0),
                )
                text_rect = text.get_rect(center=button.rect.center)
                self.screen.blit(text, text_rect)


        # TEXT ANSWER
        if question["type"] == "text":
            self.input_box = pygame.Rect(
                SCREEN_WIDTH // 2 - 200,
                420,
                400,
                60
            )
            pygame.draw.rect(self.screen, (200, 200, 200), self.input_box)

            text_surface = self.title_font.render(
                self.user_text,
                True,
                (0, 0, 0)
            )
            self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10))

        # buttons
        self.submit_button.draw(self.screen)
        self.menu_button.draw(self.screen)



