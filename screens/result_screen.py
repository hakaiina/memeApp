import pygame
from ui.button import Button
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from logic.score import ScoreCalculator


class ResultScreen:
    def __init__(self, screen, db, switch_screen, username, score, questions):
        self.screen = screen
        self.db = db
        self.switch_screen = switch_screen
        self.username = username
        self.score = score
        self.questions = questions

        if username and username != "Гость":
            self.db.update_best_score(username, score)

            self.max_score = ScoreCalculator.get_max_score(questions)
            self.percentage = ScoreCalculator.get_score_percentage(score, self.max_score)

        # Максимальный балл и процент
        self.max_score = ScoreCalculator.get_max_score(questions)
        self.percentage = ScoreCalculator.get_score_percentage(score, self.max_score)

        pygame.font.init()
        font_path = "assets/fonts/comic.ttf"

        # Шрифты
        self.title_font = pygame.font.Font(font_path, 48)
        self.score_font = pygame.font.Font(font_path, 36)
        self.message_font = pygame.font.Font(font_path, 24)
        self.button_font = pygame.font.Font(font_path, 20)

        self.bg_color = (245, 245, 245)

        # Цвета в зависимости от результата
        if self.percentage >= 80:
            self.result_color = (76, 175, 80)
            self.result_message = "Отлично!"
        elif self.percentage >= 60:
            self.result_color = (255, 193, 7)
            self.result_message = "Хорошо!"
        elif self.percentage >= 40:
            self.result_color = (255, 152, 0)
            self.result_message = "Неплохо!"
        else:
            self.result_color = (244, 67, 54)
            self.result_message = "Попробуй еще раз!"

        # Кнопки
        self.restart_button = self.create_restart_button()
        self.menu_button = self.create_menu_button()

    def create_menu_button(self):
        button_width = 220
        button_height = 60

        normal = pygame.Surface((button_width, button_height))
        normal.fill((33, 150, 243))

        text = self.button_font.render("Вернуться в меню", True, (255, 255, 255))
        text_rect = text.get_rect(center=(button_width // 2, button_height // 2))
        normal.blit(text, text_rect)

        hover = pygame.Surface((button_width, button_height))
        hover.fill((25, 118, 210))
        hover.blit(text, text_rect)

        from screens.main_screen import MainScreen

        def return_to_menu():
            main_screen = MainScreen(self.screen, self.db, self.switch_screen, self.username)
            main_screen.update_record()  # Обновляем рекорд перед отображением
            self.switch_screen(main_screen)

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT - 100),
            callback=return_to_menu
        )

    def create_restart_button(self):
        button_width = 220
        button_height = 60

        normal = pygame.Surface((button_width, button_height))
        normal.fill((76, 175, 80))

        text = self.button_font.render("Пройти еще раз", True, (255, 255, 255))
        text_rect = text.get_rect(center=(button_width // 2, button_height // 2))
        normal.blit(text, text_rect)

        hover = pygame.Surface((button_width, button_height))
        hover.fill((56, 142, 60))
        hover.blit(text, text_rect)

        from screens.quiz_screen import QuizScreen

        return Button(
            image=normal,
            hover_image=hover,
            pos=(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 100),
            callback=lambda: self.switch_screen(
                QuizScreen(self.screen, self.db, self.switch_screen, self.username)
            )
        )

    def handle_event(self, event):
        self.restart_button.handle_event(event)
        self.menu_button.handle_event(event)

    def update(self):
        self.restart_button.update()
        self.menu_button.update()

    def draw(self):

        self.screen.fill(self.bg_color)

        # Заголовок
        title_text = "Результаты теста"
        title_surface = self.title_font.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Имя пользователя
        name_text = f"{self.username}, ваш счет:"
        name_surface = self.score_font.render(name_text, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(name_surface, name_rect)

        # Счет
        score_text = f"{self.score} / {self.max_score}"
        score_surface = pygame.font.Font(None, 72).render(score_text, True, self.result_color)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(score_surface, score_rect)

        # Процент
        percent_text = f"{self.percentage:.1f}%"
        percent_surface = self.score_font.render(percent_text, True, self.result_color)
        percent_rect = percent_surface.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(percent_surface, percent_rect)

        # Сообщение о результате
        message_surface = self.message_font.render(self.result_message, True, self.result_color)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(message_surface, message_rect)

        # Круговая диаграмма (простая)
        self.draw_simple_chart()

        # Кнопки
        self.restart_button.draw(self.screen)
        self.menu_button.draw(self.screen)

        # Текст на кнопках
        restart_text = self.button_font.render("Пройти еще раз", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=self.restart_button.rect.center)
        self.screen.blit(restart_text, restart_rect)

        menu_text = self.button_font.render("Вернуться в меню", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=self.menu_button.rect.center)
        self.screen.blit(menu_text, menu_rect)

    def draw_simple_chart(self):
        center_x = SCREEN_WIDTH // 2
        center_y = 460
        radius = 50

        # Рисуем круг - фон (неправильные ответы)
        pygame.draw.circle(self.screen, (220, 220, 220), (center_x, center_y), radius)

        # Рисуем сектор правильных ответов
        if self.percentage > 0:
            angle = self.percentage * 3.6

            # Создаем поверхность для сектора
            chart_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

            # Рисуем сектор
            points = [(radius, radius)]
            for i in range(int(angle) + 1):
                rad = i * 3.14159 / 180
                x = radius + radius * pygame.math.Vector2(1, 0).rotate(i).x
                y = radius + radius * pygame.math.Vector2(1, 0).rotate(i).y
                points.append((x, y))

            if len(points) > 2:
                pygame.draw.polygon(chart_surface, self.result_color, points)

            self.screen.blit(chart_surface, (center_x - radius, center_y - radius))

        # Рисуем обводку
        pygame.draw.circle(self.screen, (100, 100, 100), (center_x, center_y), radius, 2)

        # Текст в центре
        percent_text = f"{int(self.percentage)}%"
        percent_surface = self.button_font.render(percent_text, True, (0, 0, 0))
        percent_rect = percent_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(percent_surface, percent_rect)