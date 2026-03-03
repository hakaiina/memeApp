import pygame
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SIZE


class QuizScreen:
    def __init__(self, screen, db, switch_screen):
        self.screen = screen
        self.db = db
        self.switch_screen = switch_screen

        pygame.font.init()
        self.title_font = pygame.font.Font(None, 60)
        self.font = pygame.font.Font(None, 40)

        self.bg_color = (255, 255, 255)

        # Простой тестовый вопрос (пока без БД)
        self.question = "Кто сказал: «Ну всё, я в депрессии»?"
        self.answers = [
            "Ждун",
            "Грустный кот",
            "Шлёпа",
            "Пепе"
        ]
        self.correct_index = 3

        self.selected_answer = None
        self.result_text = ""

        self.answer_buttons = self.create_answer_buttons()

    def create_answer_buttons(self):
        buttons = []

        for i, answer in enumerate(self.answers):
            normal = pygame.Surface((500, 60))
            normal.fill((200, 200, 255))

            hover = pygame.Surface((500, 60))
            hover.fill((170, 170, 240))

            btn = Button(
                image=normal,
                hover_image=hover,
                pos=(SCREEN_WIDTH // 2, 250 + i * 80),
                callback=lambda idx=i: self.check_answer(idx)
            )

            btn.text = answer  # добавим текст внутрь кнопки
            buttons.append(btn)

        return buttons

    def check_answer(self, index):
        self.selected_answer = index

        if index == self.correct_index:
            self.result_text = "Правильно! 🎉"
        else:
            self.result_text = "Неправильно 😢"

    def handle_event(self, event):
        for button in self.answer_buttons:
            button.handle_event(event)

    def update(self):
        for button in self.answer_buttons:
            button.update()

    def draw(self):
        self.screen.fill(self.bg_color)

        # Вопрос
        question_surface = self.title_font.render(
            self.question,
            True,
            (0, 0, 0)
        )
        question_rect = question_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 150)
        )

        self.screen.blit(question_surface, question_rect)

        # Кнопки
        for button in self.answer_buttons:
            button.draw(self.screen)

            # Рисуем текст поверх кнопки
            text_surface = self.font.render(
                button.text,
                True,
                (0, 0, 0)
            )
            text_rect = text_surface.get_rect(
                center=button.rect.center
            )
            self.screen.blit(text_surface, text_rect)

        # Результат
        if self.result_text:
            result_surface = self.title_font.render(
                self.result_text,
                True,
                (0, 150, 0) if self.selected_answer == self.correct_index else (200, 0, 0)
            )
            result_rect = result_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            )
            self.screen.blit(result_surface, result_rect)