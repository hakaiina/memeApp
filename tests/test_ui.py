import pytest
import pygame
import json
from unittest.mock import MagicMock, patch
from screens.quiz_screen import QuizScreen

@pytest.fixture(scope="session")
def pygame_headless():
    """Инициализирует pygame в headless режиме"""
    pygame.init()
    # Создаем минимальный дисплей
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()

class TestUI:

    @pytest.fixture(autouse=True)
    def setup_pygame(self, pygame_headless):
        """Автоматически используется для всех тестов"""
        pass

    @pytest.fixture
    def mock_screen(self):
        """Создает мок для экрана pygame"""
        screen = MagicMock()
        screen.get_width.return_value = 900
        screen.get_height.return_value = 600
        return screen

    @pytest.fixture
    def mock_db(self):
        """Создает мок для базы данных"""
        return MagicMock()

    @pytest.fixture
    def mock_switch_screen(self):
        """Создает мок для функции переключения экранов"""
        return MagicMock()

    @pytest.fixture
    def minimal_questions_file(self, tmp_path):
        """Создает минимальный JSON с одним вопросом для тестов UI"""
        test_questions = [
            {
                "type": "choice",
                "text": "Тестовый вопрос",
                "image": "test.jpg",
                "answers": ["Ответ 1", "Ответ 2", "Ответ 3"],
                "correct": [0]
            }
        ]

        questions_file = tmp_path / "questions.json"
        with open(questions_file, 'w', encoding='utf-8') as f:
            json.dump(test_questions, f)

        return questions_file

    @pytest.fixture
    def quiz_screen_ui(self, monkeypatch, mock_screen, mock_db,
                       mock_switch_screen, minimal_questions_file):
        """Создает экран викторины для UI-тестов"""

        def mock_load_questions():
            with open(minimal_questions_file, "r", encoding="utf-8") as f:
                return json.load(f)

        monkeypatch.setattr(QuizScreen, 'load_questions', staticmethod(mock_load_questions))

        quiz = QuizScreen(mock_screen, mock_db, mock_switch_screen, "test_user")

        return quiz

    def test_app_startup(self, quiz_screen_ui):
        """TC-UI-01: Запуск экрана викторины"""
        quiz = quiz_screen_ui

        # Проверяем, что экран инициализировался
        assert quiz.screen is not None
        assert quiz.db is not None
        assert quiz.username == "test_user"

        # Проверяем, что шрифты загрузились
        assert quiz.title_font is not None
        assert quiz.text_font is not None
        assert quiz.button_font is not None

        # Проверяем, что кнопки создались
        assert len(quiz.answer_btns) == 4
        assert quiz.submit_button is not None
        assert quiz.back_button is not None
        assert quiz.menu_button is not None

    def test_menu_button_functionality(self, quiz_screen_ui):
        """TC-UI-01: Работа кнопки меню"""
        quiz = quiz_screen_ui

        # Сохраняем оригинальный callback
        original_callback = quiz.menu_button.callback

        # Вызываем callback напрямую
        original_callback()

        # Проверяем, что switch_screen был вызван (для перехода в меню)
        quiz.switch_screen.assert_called_once()

    def test_answer_buttons_click(self, quiz_screen_ui):
        """TC-UI-01: Работа кнопок ответов"""
        quiz = quiz_screen_ui

        # Сохраняем оригинальный callback для первой кнопки
        original_callback = quiz.answer_btns[0].callback

        # Мокаем метод select_answer
        quiz.select_answer = MagicMock()

        # Вызываем callback напрямую с индексом 0
        original_callback()

        # Проверяем, что select_answer был вызван с правильным индексом
        quiz.select_answer.assert_called_once_with(0)

    def test_text_input_functionality(self, quiz_screen_ui):
        """TC-UI-01: Работа текстового ввода"""
        quiz = quiz_screen_ui

        # Временно подменим вопрос на текстовый для теста
        quiz.questions = [
            {
                "type": "text",
                "text": "Тестовый вопрос",
                "image": "test.jpg",
                "answer": ["правильный ответ"]
            }
        ]
        quiz.current_question = 0

        # Активируем поле ввода кликом
        mock_mouse_event = MagicMock()
        mock_mouse_event.type = pygame.MOUSEBUTTONDOWN
        mock_mouse_event.pos = (quiz.input_box.x + 10, quiz.input_box.y + 10)

        quiz.handle_event(mock_mouse_event)
        assert quiz.active_input is True

        # Создаем событие ввода текста
        mock_text_event = MagicMock()
        mock_text_event.type = pygame.KEYDOWN
        mock_text_event.key = ord('a')
        mock_text_event.unicode = 'a'

        quiz.handle_event(mock_text_event)

        # Проверяем, что текст добавился
        assert 'a' in quiz.user_text

    def test_backspace_in_text_input(self, quiz_screen_ui):
        """TC-UI-01: Работа backspace в текстовом вводе"""
        quiz = quiz_screen_ui

        # Временно подменим вопрос на текстовый
        quiz.questions = [
            {
                "type": "text",
                "text": "Тестовый вопрос",
                "image": "test.jpg",
                "answer": ["правильный ответ"]
            }
        ]
        quiz.current_question = 0

        quiz.active_input = True
        quiz.user_text = "тест"

        # Создаем событие backspace
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_BACKSPACE

        quiz.handle_event(mock_event)

        # Проверяем, что символ удалился
        assert quiz.user_text == "тес"

    def test_enter_in_text_input(self, quiz_screen_ui):
        """TC-UI-01: Нажатие Enter в текстовом поле"""
        quiz = quiz_screen_ui

        # Временно подменим вопрос на текстовый
        quiz.questions = [
            {
                "type": "text",
                "text": "Тестовый вопрос",
                "image": "test.jpg",
                "answer": ["правильный ответ"]
            }
        ]
        quiz.current_question = 0

        quiz.active_input = True
        quiz.submit_answer = MagicMock()

        # Создаем событие Enter
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_RETURN

        quiz.handle_event(mock_event)

        # Проверяем, что submit_answer был вызван
        quiz.submit_answer.assert_called_once()

    def test_text_input_limit(self, quiz_screen_ui):
        """TC-UI-01: Ограничение длины текстового ввода"""
        quiz = quiz_screen_ui

        # Временно подменим вопрос на текстовый
        quiz.questions = [
            {
                "type": "text",
                "text": "Тестовый вопрос",
                "image": "test.jpg",
                "answer": ["правильный ответ"]
            }
        ]
        quiz.current_question = 0

        quiz.active_input = True

        # Пытаемся ввести 40 символов (лимит 30)
        for i in range(40):
            mock_event = MagicMock()
            mock_event.type = pygame.KEYDOWN
            mock_event.key = ord('a')
            mock_event.unicode = 'a'
            quiz.handle_event(mock_event)

        # Проверяем, что длина не превышает 30
        assert len(quiz.user_text) <= 30

    def test_all_buttons_created(self, quiz_screen_ui):
        """TC-UI-01: Проверка создания всех кнопок"""
        quiz = quiz_screen_ui

        # Проверяем наличие всех необходимых кнопок
        assert hasattr(quiz, 'answer_btns')
        assert hasattr(quiz, 'submit_button')
        assert hasattr(quiz, 'back_button')
        assert hasattr(quiz, 'menu_button')

        # Проверяем количество кнопок ответов
        assert len(quiz.answer_btns) == 4

        # Проверяем, что у каждой кнопки есть callback
        for btn in quiz.answer_btns:
            assert btn.callback is not None

        assert quiz.submit_button.callback is not None
        assert quiz.back_button.callback is not None
        assert quiz.menu_button.callback is not None

    def test_draw_method_calls(self, quiz_screen_ui):
        """TC-UI-01: Проверка отрисовки экрана"""
        quiz = quiz_screen_ui

        # Сбрасываем счетчики вызовов
        quiz.screen.reset_mock()

        # Вызываем метод отрисовки
        quiz.draw()

        # Проверяем, что screen.fill был вызван
        quiz.screen.fill.assert_called_once_with(quiz.bg_color)

        # Проверяем, что blit вызывался (для текста, кнопок и т.д.)
        assert quiz.screen.blit.call_count > 0

    def test_update_method(self, quiz_screen_ui):
        """TC-UI-01: Проверка метода обновления"""
        quiz = quiz_screen_ui

        # Создаем реальные кнопки, но мокаем их методы update
        for btn in quiz.answer_btns:
            btn.update = MagicMock()

        quiz.submit_button.update = MagicMock()
        quiz.back_button.update = MagicMock()
        quiz.menu_button.update = MagicMock()

        # Вызываем update
        quiz.update()

        # Проверяем, что все кнопки обновились
        for btn in quiz.answer_btns:
            btn.update.assert_called_once()

        quiz.submit_button.update.assert_called_once()
        quiz.back_button.update.assert_called_once()
        quiz.menu_button.update.assert_called_once()

    def test_cursor_blinking(self, quiz_screen_ui):
        """TC-UI-01: Проверка мигания курсора"""
        quiz = quiz_screen_ui

        # Изначально курсор видим
        assert quiz.cursor_visible is True
        assert quiz.cursor_timer == 0

        # Обновляем несколько раз
        for i in range(31):
            quiz.update()

        # После 30 тиков курсор должен мигнуть
        # Может быть True или False в зависимости от четности
        assert quiz.cursor_timer < 30

    def test_wrap_text_function(self, quiz_screen_ui):
        """TC-UI-01: Проверка функции переноса текста"""
        quiz = quiz_screen_ui

        long_text = "Это очень длинный текст, который должен быть разбит на несколько строк при отображении на экране"

        lines = quiz.wrap_text(long_text, quiz.title_font, 200)

        # Проверяем, что текст разбился на несколько строк
        assert len(lines) > 1
        assert isinstance(lines, list)
        assert all(isinstance(line, str) for line in lines)
