class ScoreCalculator:

    # Веса для разных типов вопросов
    WEIGHTS = {
        "choice": 1,
        "text": 2
    }

    @staticmethod
    def calculate_score(question_type, user_answer, correct_answers):
        if question_type == "choice":
            return ScoreCalculator._calculate_choice_score(user_answer, correct_answers)
        elif question_type == "text":
            return ScoreCalculator._calculate_text_score(user_answer, correct_answers)
        return 0

    @staticmethod
    def _calculate_choice_score(selected_answers, correct_answers):
        if not selected_answers:
            return 0

        selected_set = set(selected_answers)
        correct_set = set(correct_answers)

        if selected_set == correct_set:
            return ScoreCalculator.WEIGHTS["choice"]

        return 0

    @staticmethod
    def _calculate_text_score(user_text, correct_answers):
        if not user_text:
            return 0

        user_answer = user_text.lower().strip()

        # correct_answers всегда список возможных правильных ответов
        for answer in correct_answers:
            if user_answer == answer.lower().strip():
                return ScoreCalculator.WEIGHTS["text"]

        return 0

    @staticmethod
    def get_max_score(questions):
        total = 0
        for question in questions:
            question_type = question.get("type")
            total += ScoreCalculator.WEIGHTS.get(question_type, 0)
        return total

    @staticmethod
    def get_score_percentage(score, max_score):
        """
        Получить процент правильных ответов

        Args:
            score (int): Набранные баллы
            max_score (int): Максимальный балл

        Returns:
            float: Процент правильных ответов
        """
        if max_score == 0:
            return 0
        return (score / max_score) * 100