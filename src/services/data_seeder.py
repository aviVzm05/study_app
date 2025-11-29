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

        # Math Questions (examples for decimals)
        Question(topic_id=math_topic.id, question_type="multiple_choice",
                                 prompt="What is 0.5 as a fraction?", options='["1/2", "1/4", "1/5"]',
                                 correct_answer="1/2").save()
        Question(topic_id=math_topic.id, question_type="multiple_choice",
                                 prompt="Convert 0.75 to a fraction.", options='["3/4", "1/4", "7/10"]',
                                 correct_answer="3/4").save()
        Question(topic_id=math_topic.id, question_type="multiple_choice",
                                 prompt="Which is greater: 0.2 or 0.02?", options='["0.2", "0.02"]',
                                 correct_answer="0.2").save()

        # English Questions (examples for nouns)
        Question(topic_id=english_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence using a common noun.", correct_answer="[VALIDATION_RULE: common noun present]").save()
        Question(topic_id=english_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence that includes two proper nouns.", correct_answer="[VALIDATION_RULE: two proper nouns present]").save()
        Question(topic_id=english_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence about your favorite animal.", correct_answer="[VALIDATION_RULE: describes favorite animal]").save()
        
    print("Initial data seeded successfully.")

if __name__ == '__main__':
    seed_initial_data()
