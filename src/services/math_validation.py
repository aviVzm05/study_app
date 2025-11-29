class MathValidationService:
    def __init__(self):
        pass

    def validate_answer(self, question_type, user_answer, correct_answer):
        """
        Validates a user's answer against the correct answer.
        This can be extended for different question types and more sophisticated validation.
        """
        if question_type == "multiple_choice":
            return user_answer.strip() == correct_answer.strip()
        elif question_type == "fill_in_the_blank":
            return user_answer.strip().lower() == correct_answer.strip().lower()
        # Add more validation logic for other question types as needed
        return False

    def get_feedback(self, is_correct, correct_answer):
        """Provides feedback to the user based on correctness."""
        if is_correct:
            return "<font color='green'>Correct!</font>"
        else:
            return f"<font color='red'>Incorrect. The correct answer was: {correct_answer}</font>"
