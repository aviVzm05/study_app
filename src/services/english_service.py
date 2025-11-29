from models.models import Lesson, Question, Topic

class EnglishService:
    def __init__(self):
        pass

    def get_lesson_and_questions_for_topic(self, topic_id):
        """Retrieves lesson and associated questions for a given topic ID."""
        lesson = next((l for l in Lesson.find_all() if l.topic_id == topic_id), None)
        questions = [q for q in Question.find_all() if q.topic_id == topic_id and q.question_type == 'sentence_construction']
        return lesson, questions

    def get_topics_for_grade_subject(self, grade, subject_id):
        """Retrieves English topics for a given grade and subject ID."""
        return [t for t in Topic.find_all() if t.grade == grade and t.subject_id == subject_id and "English" in t.name]
