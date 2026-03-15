import pytest
import pygame
import json
import os
from unittest.mock import MagicMock, patch, mock_open
from screens.quiz_screen import QuizScreen


class TestQuestions:

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
        db = MagicMock()
        return db

    @pytest.fixture
    def mock_switch_screen(self):
        """Создает мок для функции переключения экранов"""
        return MagicMock()

    @pytest.fixture
    def test_questions_file(self, tmp_path):
        """Создает временный JSON-файл с тестовыми вопросами"""
        test_questions = [
            {
                "type": "choice",
                "text": "'Одержимость(Whiplash)' - великолепный фильм, но и здесь не обошлось без мемов, в одном из которых фигурирует фраза, которую вечно говорил Флетчер",
                "image": "assets/images/whiplash.jpg",
                "answers": [
                    "Were you rushing or dragging? (Ты частил или мямлил?)",
                    "No quite my tempo (Не мой темп)",
                    "In four, damn it. Look at me (На четыре, черт возьми. Смотри на меня)"
                ],
                "correct": [1]
            },
            {
                "type": "text",
                "text": "Кто звонит?",
                "image": "assets/images/nisheta.jpg",
                "answer": ["смерть в нищете", "нищета"]
            }
        ]

        questions_file = tmp_path / "questions.json"
        with open(questions_file, 'w', encoding='utf-8') as f:
            json.dump(test_questions, f, ensure_ascii=False, indent=2)

        return questions_file

    @pytest.fixture
    def quiz_screen_with_test_questions(self, monkeypatch, mock_screen, mock_db,
                                        mock_switch_screen, test_questions_file):
        """Создает экран викторины с тестовыми вопросами"""

        # Подменяем путь к файлу вопросов в методе load_questions
        original_load = QuizScreen.load_questions

        def mock_load_questions():
            with open(test_questions_file, "r", encoding="utf-8") as f:
                return json.load(f)

        monkeypatch.setattr(QuizScreen, 'load_questions', staticmethod(mock_load_questions))

        # Создаем экран викторины
        quiz = QuizScreen(mock_screen, mock_db, mock_switch_screen, "test_user")

        return quiz

    def test_load_questions_from_file(self, quiz_screen_with_test_questions, test_questions_file):
        """TC-Q-01: Загрузка вопросов из JSON файла"""
        quiz = quiz_screen_with_test_questions

        # Проверяем, что вопросы загрузились
        assert len(quiz.questions) == 2

        # Проверяем первый вопрос (choice)
        assert quiz.questions[0]["type"] == "choice"
        assert "Whiplash" in quiz.questions[0]["text"]
        assert len(quiz.questions[0]["answers"]) == 3
        assert quiz.questions[0]["correct"] == [1]

        # Проверяем второй вопрос (text)
        assert quiz.questions[1]["type"] == "text"
        assert quiz.questions[1]["text"] == "Кто звонит?"
        assert len(quiz.questions[1]["answer"]) == 2
        assert "смерть в нищете" in quiz.questions[1]["answer"]

    def test_display_choice_question(self, quiz_screen_with_test_questions):
        """TC-Q-01: Отображение вопроса с вариантами выбора"""
        quiz = quiz_screen_with_test_questions

        # Убеждаемся, что текущий вопрос - choice
        assert quiz.questions[quiz.current_question]["type"] == "choice"

        # Проверяем создание кнопок для ответов
        assert len(quiz.answer_btns) == 4  # Создается 4 кнопки по умолчанию

        # Проверяем, что выбранных ответов нет
        assert quiz.selected_answers == []

        # Имитируем выбор ответа
        quiz.select_answer(0)
        assert 0 in quiz.selected_answers

        # Проверяем, что можно выбрать другой ответ (для choice с одним правильным)
        quiz.select_answer(1)
        assert quiz.selected_answers == [1]  # Должен замениться

    def test_display_text_question(self, quiz_screen_with_test_questions):
        """TC-Q-01: Отображение вопроса с текстовым ответом"""
        quiz = quiz_screen_with_test_questions

        # Переходим ко второму вопросу (text)
        quiz.current_question = 1

        # Проверяем тип вопроса
        assert quiz.questions[1]["type"] == "text"

        # Проверяем наличие поля ввода
        assert hasattr(quiz, 'input_box')
        assert quiz.input_box.width == 300
        assert quiz.input_box.height == 50

        # Проверяем начальное состояние
        assert quiz.user_text == ""
        assert quiz.active_input is False

    def test_submit_choice_answer_correct(self, quiz_screen_with_test_questions):
        """TC-Q-02: Проверка правильного ответа для choice вопроса"""
        quiz = quiz_screen_with_test_questions

        # Выбираем правильный ответ (индекс 1)
        quiz.select_answer(1)
        quiz.submit_answer()

        # Проверяем, что счет увеличился
        assert quiz.score > 0

        # Проверяем, что ответ сохранился
        assert quiz.user_answers[0] == [1]

        # Проверяем, что перешли к следующему вопросу
        assert quiz.current_question == 1

    def test_submit_choice_answer_wrong(self, quiz_screen_with_test_questions):
        """TC-Q-02: Проверка неправильного ответа для choice вопроса"""
        quiz = quiz_screen_with_test_questions
        initial_score = quiz.score

        # Выбираем неправильный ответ (индекс 0 вместо 1)
        quiz.select_answer(0)
        quiz.submit_answer()

        # Проверяем, что счет не увеличился
        assert quiz.score == initial_score

        # Проверяем, что ответ сохранился
        assert quiz.user_answers[0] == [0]

        # Проверяем, что перешли к следующему вопросу
        assert quiz.current_question == 1

    def test_submit_text_answer_correct(self, quiz_screen_with_test_questions):
        """TC-Q-02: Проверка правильного ответа для text вопроса"""
        quiz = quiz_screen_with_test_questions

        # Переходим ко второму вопросу
        quiz.current_question = 1

        # Вводим правильный ответ
        quiz.user_text = "смерть в нищете"
        quiz.submit_answer()

        # Проверяем, что счет увеличился
        assert quiz.score > 0

        # Проверяем, что ответ сохранился
        assert quiz.user_answers[1] == "смерть в нищете"

    def test_submit_text_answer_wrong(self, quiz_screen_with_test_questions):
        """TC-Q-02: Проверка неправильного ответа для text вопроса"""
        quiz = quiz_screen_with_test_questions

        # Переходим ко второму вопросу
        quiz.current_question = 1
        initial_score = quiz.score

        # Вводим неправильный ответ
        quiz.user_text = "неправильный ответ"
        quiz.submit_answer()

        # Проверяем, что счет не увеличился
        assert quiz.score == initial_score

    def test_submit_text_answer_case_insensitive(self, quiz_screen_with_test_questions):
        """TC-Q-02: Проверка регистронезависимости текстовых ответов"""
        quiz = quiz_screen_with_test_questions

        # Переходим ко второму вопросу
        quiz.current_question = 1

        # Проверяем разные варианты регистра
        test_variants = [
            "СМЕРТЬ В НИЩЕТЕ",
            "Смерть В Нищете",
            "смерть в нищете",
            "НИЩЕТА",
            "Нищета"
        ]

        for variant in test_variants:
            quiz.user_text = variant
            quiz.submit_answer()
            assert quiz.score > 0
            quiz.score = 0  # Сбрасываем для следующей проверки
            quiz.current_question = 1  # Возвращаемся к вопросу

    def test_go_back_to_previous_question(self, quiz_screen_with_test_questions):
        """TC: Возврат к предыдущему вопросу"""
        quiz = quiz_screen_with_test_questions

        # Отвечаем на первый вопрос
        quiz.select_answer(1)
        quiz.submit_answer()

        # Проверяем, что перешли ко второму
        assert quiz.current_question == 1

        # Возвращаемся назад
        quiz.go_back()

        # Проверяем, что вернулись к первому
        assert quiz.current_question == 0

        # Проверяем, что ответ сохранился
        assert quiz.selected_answers == [1]

    def test_question_progress_display(self, quiz_screen_with_test_questions):
        """TC: Отображение прогресса вопросов"""
        quiz = quiz_screen_with_test_questions

        # Проверяем отрисовку прогресса
        quiz.draw()

        # Проверяем, что метод отрисовки был вызван
        quiz.screen.blit.assert_called()

    def test_multiple_correct_answers_choice(self, monkeypatch, mock_screen, mock_db,
                                             mock_switch_screen, tmp_path):
        """TC: Вопрос с несколькими правильными ответами"""
        # Создаем вопрос с несколькими правильными ответами
        test_questions = [
            {
                "type": "choice",
                "text": "Выберите все правильные варианты",
                "image": "test.jpg",
                "answers": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
                "correct": [0, 2]  # Два правильных ответа
            }
        ]

        questions_file = tmp_path / "questions.json"
        with open(questions_file, 'w', encoding='utf-8') as f:
            json.dump(test_questions, f)

        def mock_load():
            with open(questions_file, "r", encoding="utf-8") as f:
                return json.load(f)

        monkeypatch.setattr(QuizScreen, 'load_questions', staticmethod(mock_load))

        quiz = QuizScreen(mock_screen, mock_db, mock_switch_screen, "test_user")

        # Выбираем только один правильный ответ
        quiz.select_answer(0)
        quiz.submit_answer()

        # Должен получить частичные баллы (зависит от ScoreCalculator)
        # Здесь мы просто проверяем, что ответ сохранился
        assert quiz.user_answers[0] == [0]