import pygame
import json
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from logic.score import ScoreCalculator


class QuizScreen:
    def __init__(self, screen, db, switch_screen, username):
        self.screen = screen
        self.db = db
        self.switch_screen = switch_screen
        self.username = username

        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"

        self.title_font = pygame.font.Font(font_path, 24)
        self.text_font = pygame.font.Font(font_path, 18)
        self.button_font = pygame.font.Font(font_path, 16)

        self.bg_color = (245, 245, 245)

        # Загрузка вопросов
        self.questions = self.load_questions()
        self.current_question = 0
        self.score = 0

        # Выбранные ответы
        self.selected_answers = []
        self.user_text = ""

        # Сохранение ответов пользователя
        self.user_answers = [None] * len(self.questions)

        # Поле ввода
        self.input_box = pygame.Rect(
            SCREEN_WIDTH // 2 - 150,
            400,
            300,
            50
        )
        self.active_input = False

        # Курсор
        self.cursor_visible = True
        self.cursor_timer = 0

        # Кнопки
        self.answer_btns = []
        self.create_answer_buttons()

        self.submit_button = self.create_submit_button()
        self.back_button = self.create_back_button()
        self.menu_button = self.create_menu_button()

        self.image_cache = {}

    @staticmethod
    def load_questions():
        with open("db/questions.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def create_answer_buttons(self):
        """Создает кнопки для вариантов ответов"""
        button_width = 500
        button_height = 50

        for i in range(4):
            normal = pygame.Surface((button_width, button_height))
            normal.fill((200, 200, 255))

            hover = pygame.Surface((button_width, button_height))
            hover.fill((170, 170, 240))

            btn = Button(
                image=normal,
                hover_image=hover,
                pos=(SCREEN_WIDTH // 2, 300 + i * 60),
                callback=lambda idx=i: self.select_answer(idx)
            )
            self.answer_btns.append(btn)

    def create_submit_button(self):
        """Зеленая кнопка отправки"""
        button_width = 140
        button_height = 40

        normal = pygame.Surface((button_width, button_height))
        normal.fill((120, 200, 120))

        hover = pygame.Surface((button_width, button_height))
        hover.fill((100, 180, 100))

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT - 50),  # Изменил позицию
            callback=self.submit_answer
        )

    def create_back_button(self):
        """Желтая кнопка назад"""
        button_width = 140
        button_height = 40

        normal = pygame.Surface((button_width, button_height))
        normal.fill((255, 200, 100))

        hover = pygame.Surface((button_width, button_height))
        hover.fill((235, 180, 80))

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50),  # Изменил позицию
            callback=self.go_back
        )

    def create_menu_button(self):
        """Красная кнопка меню"""
        button_width = 140
        button_height = 40

        normal = pygame.Surface((button_width, button_height))
        normal.fill((255, 150, 150))

        hover = pygame.Surface((button_width, button_height))
        hover.fill((235, 130, 130))

        from screens.main_screen import MainScreen

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2 + 160, SCREEN_HEIGHT - 50),  # Изменил позицию
            callback=lambda: self.switch_screen(
                MainScreen(self.screen, self.db, self.switch_screen, self.username)
            )
        )

    def select_answer(self, index):
        """Выбор ответа"""
        question = self.questions[self.current_question]

        if len(question["correct"]) > 1:
            if index in self.selected_answers:
                self.selected_answers.remove(index)
            else:
                self.selected_answers.append(index)
        else:
            self.selected_answers = [index]

    def submit_answer(self):
        question = self.questions[self.current_question]

        # Подсчет баллов через ScoreCalculator
        if question["type"] == "choice":
            points = ScoreCalculator.calculate_score(
                "choice",
                self.selected_answers,
                question["correct"]
            )
        else:  # text
            points = ScoreCalculator.calculate_score(
                "text",
                self.user_text,
                question["answer"]
            )

        self.score += points

        # Сохраняем ответ
        if question["type"] == "choice":
            self.user_answers[self.current_question] = list(self.selected_answers)
        else:
            self.user_answers[self.current_question] = self.user_text

        # Переход к следующему вопросу
        self.selected_answers = []
        self.user_text = ""
        self.active_input = False
        self.current_question += 1

        if self.current_question >= len(self.questions):
            # Переходим на экран результатов
            from screens.result_screen import ResultScreen
            self.switch_screen(
                ResultScreen(
                    self.screen,
                    self.db,
                    self.switch_screen,
                    self.username,
                    self.score,
                    self.questions
                )
            )

    def go_back(self):
        """Возврат к предыдущему вопросу"""
        if self.current_question == 0:
            return

        self.current_question -= 1
        previous = self.user_answers[self.current_question]
        question = self.questions[self.current_question]

        if question["type"] == "choice":
            self.selected_answers = previous if previous else []
        else:
            self.user_text = previous if previous else ""
        self.active_input = False

    def handle_event(self, event):
        if self.current_question >= len(self.questions):
            return

        question = self.questions[self.current_question]

        if question["type"] == "choice":
            for btn in self.answer_btns:
                btn.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active_input = self.input_box.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.submit_answer()
                elif len(self.user_text) < 30:
                    self.user_text += event.unicode

        self.submit_button.handle_event(event)
        self.back_button.handle_event(event)
        self.menu_button.handle_event(event)

    def update(self):
        """Обновление состояния"""
        for btn in self.answer_btns:
            btn.update()

        self.submit_button.update()
        self.back_button.update()
        self.menu_button.update()

        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self):
        """Отрисовка экрана"""
        self.screen.fill(self.bg_color)

        if self.current_question >= len(self.questions):
            return

        question = self.questions[self.current_question]

        # Номер вопроса
        progress = f"{self.current_question + 1} / {len(self.questions)}"
        progress_text = self.title_font.render(progress, True, (100, 100, 100))
        self.screen.blit(progress_text, (20, 15))

        # Текст вопроса
        question_lines = self.wrap_text(
            question["text"],
            self.title_font,
            500
        )

        # Рисуем вопрос построчно
        y_offset = 50
        for line in question_lines:
            text_surface = self.title_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(midtop=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30

        # Изображение
        try:
            if question["image"] not in self.image_cache:
                img = pygame.image.load(question["image"]).convert_alpha()
                # Масштабируем под окно 900x600
                img = pygame.transform.scale(img, (350, 200))
                self.image_cache[question["image"]] = img

            image = self.image_cache[question["image"]]
            image_y = y_offset + 10  # Уменьшил отступ
            image_rect = image.get_rect(midtop=(SCREEN_WIDTH // 2, image_y))
            self.screen.blit(image, image_rect)

            answers_start_y = image_rect.bottom + 30
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            answers_start_y = y_offset + 10

        # Отрисовка ответов
        if question["type"] == "choice":
            self.draw_choice_answers(question, answers_start_y)
        else:
            self.draw_text_answer(answers_start_y)

        # Навигационные кнопки
        self.draw_navigation_buttons()

    def wrap_text(self, text, font, max_width):
        """Разбивает текст на строки по ширине"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_choice_answers(self, question, start_y):
        """Отрисовка вариантов ответов"""
        for i, btn in enumerate(self.answer_btns[:len(question["answers"])]):
            # Позиционируем кнопку
            btn.rect.center = (SCREEN_WIDTH // 2, start_y + i * 60)

            # Рисуем кнопку
            btn.draw(self.screen)

            # Рисуем текст на кнопке
            answer_text = f"{i + 1}. {question['answers'][i]}"

            if self.text_font.size(answer_text)[0] > btn.rect.width - 20:
                lines = self.wrap_text(answer_text, self.text_font, btn.rect.width - 20)
                y_offset = btn.rect.centery - (len(lines) * self.text_font.get_height() // 2)

                for line in lines:
                    line_surface = self.text_font.render(line, True, (0, 0, 0))
                    line_rect = line_surface.get_rect(centerx=btn.rect.centerx, y=y_offset)
                    self.screen.blit(line_surface, line_rect)
                    y_offset += self.text_font.get_height()
            else:
                text_surface = self.text_font.render(answer_text, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=btn.rect.center)
                self.screen.blit(text_surface, text_rect)

            # Подсветка выбранного ответа
            if i in self.selected_answers:
                pygame.draw.rect(self.screen, (100, 150, 255), btn.rect, 3)

    def draw_text_answer(self, start_y):
        """Отрисовка текстового ответа"""
        self.input_box.y = start_y

        # Рисуем поле ввода
        color = (230, 230, 250) if self.active_input else (255, 255, 255)
        pygame.draw.rect(self.screen, color, self.input_box)
        pygame.draw.rect(self.screen, (150, 150, 150), self.input_box, 2)

        # Рисуем текст или placeholder
        if self.user_text == "" and not self.active_input:
            placeholder = self.text_font.render("Введите ответ...", True, (150, 150, 150))
            self.screen.blit(placeholder, (self.input_box.x + 10, self.input_box.y + 15))
        else:
            display_text = self.user_text
            if self.active_input and self.cursor_visible:
                display_text += "|"

            if self.text_font.size(display_text)[0] > self.input_box.width - 20:
                while self.text_font.size(display_text + "...")[0] > self.input_box.width - 20:
                    display_text = display_text[:-1]
                display_text += "..."

            text_surface = self.text_font.render(display_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 15))

    def draw_navigation_buttons(self):
        """Отрисовка навигационных кнопок"""
        bottom_y = SCREEN_HEIGHT - 60

        # Кнопка "Назад"
        self.back_button.rect.center = (SCREEN_WIDTH // 2 - 180, bottom_y)
        self.back_button.draw(self.screen)
        back_text = self.button_font.render("Назад", True, (0, 0, 0))
        back_rect = back_text.get_rect(center=self.back_button.rect.center)
        self.screen.blit(back_text, back_rect)

        # Кнопка "Отправить"
        self.submit_button.rect.center = (SCREEN_WIDTH // 2, bottom_y)
        self.submit_button.draw(self.screen)
        submit_text = self.button_font.render("Отправить", True, (0, 0, 0))
        submit_rect = submit_text.get_rect(center=self.submit_button.rect.center)
        self.screen.blit(submit_text, submit_rect)

        # Кнопка "В меню"
        self.menu_button.rect.center = (SCREEN_WIDTH // 2 + 180, bottom_y)
        self.menu_button.draw(self.screen)
        menu_text = self.button_font.render("В меню", True, (0, 0, 0))
        menu_rect = menu_text.get_rect(center=self.menu_button.rect.center)
        self.screen.blit(menu_text, menu_rect)