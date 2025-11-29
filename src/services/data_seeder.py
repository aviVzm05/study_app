from services.database import execute_query
from models.models import Subject, Topic, Lesson, Question
from datetime import datetime

def seed_initial_data():
    """Seeds the database with initial content based on MVP requirements."""
    # Ensure schema is created before seeding
    from models.schema import create_schema
    create_schema()

    # Clear existing data for idempotent seeding (for development)
    execute_query("DELETE FROM progress")
    execute_query("DELETE FROM questions")
    execute_query("DELETE FROM lessons")
    execute_query("DELETE FROM topics")
    execute_query("DELETE FROM subjects")

    # Seed Subjects
    math_subject = Subject(name="Mathematics")
    math_subject.save()
    english_subject = Subject(name="English")
    english_subject.save()

    # Seed one topic per subject per grade (5-10)
    for grade in range(5, 11):
        # Math Topic: Decimals (example)
        math_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Decimals")
        math_topic.save()

        # Math Lesson
        math_lesson = Lesson(topic_id=math_topic.id, title=f"Understanding Decimals (Grade {grade})",
                             content="""Decimals are a way of writing numbers that are not whole numbers. They are based on powers of ten...""")
        math_lesson.save()

        # Math Question (example for decimals)
        math_question = Question(topic_id=math_topic.id, question_type="multiple_choice",
                                 prompt="What is 0.5 as a fraction?", options='["1/2", "1/4", "1/5"]',
                                 correct_answer="1/2")
        math_question.save()

        # English Topic: Nouns (example)
        english_topic = Topic(subject_id=english_subject.id, grade=grade, name=f"English - Grade {grade} Nouns")
        english_topic.save()

        # English Lesson
        english_lesson = Lesson(topic_id=english_topic.id, title=f"Exploring Nouns (Grade {grade})",
                                content="""A noun is a word that names something: a person, place, thing, or idea...""")
        english_lesson.save()

        # English Question (example for nouns)
        english_question = Question(topic_id=english_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence using a common noun.", correct_answer="[VALIDATION_RULE: common noun present]")
        english_question.save()
        
    print("Initial data seeded successfully.")

if __name__ == '__main__':
    seed_initial_data()
