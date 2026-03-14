class ScoreCalculator:

    WEIGHTS = {
        "choice": 1,
        "text": 3
    }

    @staticmethod
    def calculate_score(question_type, user_answer, correct_answers, selected_index=None):
        if question_type == "choice":
            return ScoreCalculator._calculate_choice_score(user_answer, correct_answers)
        elif question_type == "text":
            return ScoreCalculator._calculate_text_score(user_answer, correct_answers)
        return 0

    @staticmethod
    def _calculate_choice_score(selected_index, correct_answers):
        if selected_index is None:
            return 0

        if isinstance(correct_answers, list):
            if selected_index in correct_answers:
                return ScoreCalculator.WEIGHTS["choice"]
        else:
            if selected_index == correct_answers:
                return ScoreCalculator.WEIGHTS["choice"]

        return 0

    @staticmethod
    def _calculate_text_score(user_text, correct_answers):
        if not user_text:
            return 0

        user_answer = user_text.lower().strip()

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
        if max_score == 0:
            return 0
        return (score / max_score) * 100


def calculate_score(question_type, user_answer, correct_answers):
    return ScoreCalculator.calculate_score(question_type, user_answer, correct_answers)