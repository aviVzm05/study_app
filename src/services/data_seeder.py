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
        # Existing Math Topic: Decimals
        math_decimals_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Decimals")
        math_decimals_topic.save()

        Lesson(topic_id=math_decimals_topic.id, title=f"Understanding Decimals (Grade {grade})",
                             content="""Decimals are a way of writing numbers that are not whole numbers. They are based on powers of ten...""").save()

        # Math Questions for Decimals
        Question(topic_id=math_decimals_topic.id, question_type="multiple_choice",
                                 prompt="What is 0.5 as a fraction?", options='["1/2", "1/4", "1/5"]',
                                 correct_answer="1/2").save()
        Question(topic_id=math_decimals_topic.id, question_type="multiple_choice",
                                 prompt="Convert 0.75 to a fraction.", options='["3/4", "1/4", "7/10"]',
                                 correct_answer="3/4").save()
        Question(topic_id=math_decimals_topic.id, question_type="multiple_choice",
                                 prompt="Which is greater: 0.2 or 0.02?", options='["0.2", "0.02"]',
                                 correct_answer="0.2").save()

        # Existing English Topic: Nouns
        english_nouns_topic = Topic(subject_id=english_subject.id, grade=grade, name=f"English - Grade {grade} Nouns")
        english_nouns_topic.save()

        Lesson(topic_id=english_nouns_topic.id, title=f"Exploring Nouns (Grade {grade})",
                                content="""A noun is a word that names something: a person, place, thing, or idea...""").save()

        # English Questions for Nouns
        Question(topic_id=english_nouns_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence using a common noun.", correct_answer="[VALIDATION_RULE: common noun present]").save()
        Question(topic_id=english_nouns_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence that includes two proper nouns.", correct_answer="[VALIDATION_RULE: two proper nouns present]").save()
        Question(topic_id=english_nouns_topic.id, question_type="sentence_construction",
                                   prompt="Write a sentence about your favorite animal.", correct_answer="[VALIDATION_RULE: describes favorite animal]").save()
        
        # Add specific 7th Grade Math topics and questions from PDF
        if grade == 7:
            # Integers Topic
            math_integers_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Integers")
            math_integers_topic.save()
            Lesson(topic_id=math_integers_topic.id, title=f"Operations on Integers (Grade {grade})",
                   content="""Integers include all positive and negative whole numbers, and zero. Operations like addition, subtraction, multiplication, and division follow specific rules based on the signs of the numbers.""").save()
            Question(topic_id=math_integers_topic.id, question_type="multiple_choice",
                                     prompt="What is 10 + 8?", options='["18", "2", "-18"]', correct_answer="18").save()
            Question(topic_id=math_integers_topic.id, question_type="multiple_choice",
                                     prompt="What is -6 - 9?", options='["15", "-15", "3"]', correct_answer="-15").save()
            Question(topic_id=math_integers_topic.id, question_type="multiple_choice",
                                     prompt="What is -7 + 13?", options='["20", "-20", "6"]', correct_answer="6").save()
            Question(topic_id=math_integers_topic.id, question_type="multiple_choice",
                                     prompt="What is 13 - (-5)?", options='["8", "18", "-8"]', correct_answer="18").save()
            Question(topic_id=math_integers_topic.id, question_type="multiple_choice",
                                     prompt="What is -6 x -4?", options='["-24", "24", "10"]', correct_answer="24").save()
            Question(topic_id=math_integers_topic.id, question_type="multiple_choice",
                                     prompt="What is 12 ÷ -4?", options='["3", "-3", "-16"]', correct_answer="-3").save()

            # Rational Numbers Topic
            math_rational_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Rational Numbers")
            math_rational_topic.save()
            Lesson(topic_id=math_rational_topic.id, title=f"Operations on Rational Numbers (Grade {grade})",
                   content="""Rational numbers can be represented as p/q where q is not zero. Operations like addition, subtraction, multiplication, and division follow specific rules for fractions.""").save()
            Question(topic_id=math_rational_topic.id, question_type="multiple_choice",
                                     prompt="What is 2/3 + 5/4?", options='["7/7", "23/12", "10/12"]', correct_answer="23/12").save()
            Question(topic_id=math_rational_topic.id, question_type="multiple_choice",
                                     prompt="What is 7/3 - 5/3?", options='["2/3", "12/3", "2/6"]', correct_answer="2/3").save()
            Question(topic_id=math_rational_topic.id, question_type="multiple_choice",
                                     prompt="What is 2/3 x 8/6?", options='["16/18", "1/3", "16/9"]', correct_answer="16/9").save()
            Question(topic_id=math_rational_topic.id, question_type="multiple_choice",
                                     prompt="What is 2/3 ÷ 1/5?", options='["10/3", "2/15", "1/3"]', correct_answer="10/3").save()

            # Geometry Topic
            math_geometry_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Geometry")
            math_geometry_topic.save()
            Lesson(topic_id=math_geometry_topic.id, title=f"Lines, Angles, and Shapes (Grade {grade})",
                   content="""Geometry involves the study of shapes, sizes, positions, and properties of space. This includes understanding lines, angles, and calculating perimeter and area.""").save()
            Question(topic_id=math_geometry_topic.id, question_type="multiple_choice",
                                     prompt="An angle less than 90 degrees is called?", options='["Obtuse", "Acute", "Right"]', correct_answer="Acute").save()
            Question(topic_id=math_geometry_topic.id, question_type="multiple_choice",
                                     prompt="What is the sum of complementary angles?", options='["90°", "180°", "360°"]', correct_answer="90°").save()
            Question(topic_id=math_geometry_topic.id, question_type="multiple_choice",
                                     prompt="What is the perimeter of a rectangle with length 12cm and breadth 8cm?", options='["20cm", "40cm", "96cm²"]', correct_answer="40cm").save()
            Question(topic_id=math_geometry_topic.id, question_type="multiple_choice",
                                     prompt="What is the area of a square with side 6cm?", options='["12cm", "24cm", "36cm²"]', correct_answer="36cm²").save()

            # Algebra Topic
            math_algebra_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Algebra")
            math_algebra_topic.save()
            Lesson(topic_id=math_algebra_topic.id, title=f"Algebraic Expressions and Equations (Grade {grade})",
                   content="""Algebra uses letters (variables) to represent numbers. Algebraic expressions combine variables and numbers using operations, while equations involve an equal sign.""").save()
            Question(topic_id=math_algebra_topic.id, question_type="multiple_choice",
                                     prompt="In '5x - 3', '5' is the:", options='["Variable", "Coefficient", "Constant"]', correct_answer="Coefficient").save()
            Question(topic_id=math_algebra_topic.id, question_type="multiple_choice",
                                     prompt="An equation has an ______ sign.", options='["addition", "multiplication", "equal"]', correct_answer="equal").save()
            Question(topic_id=math_algebra_topic.id, question_type="fill_in_the_blank",
                                     prompt="If 5x + 1 = 3x + 5, then x = ____.", correct_answer="2").save()

            # Data Handling Topic
            math_data_handling_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Data Handling")
            math_data_handling_topic.save()
            Lesson(topic_id=math_data_handling_topic.id, title=f"Mean, Median, and Mode (Grade {grade})",
                   content="""Data handling involves collecting, organizing, and analyzing data. Mean, Median, and Mode are measures of central tendency.""").save()
            Question(topic_id=math_data_handling_topic.id, question_type="multiple_choice",
                                     prompt="What is the mean of 12, 18, 20, 15, 25?", options='["18", "15", "20"]', correct_answer="18").save()
            Question(topic_id=math_data_handling_topic.id, question_type="multiple_choice",
                                     prompt="What is the median of 7, 3, 9, 5, 11?", options='["7", "9", "5"]', correct_answer="7").save()
            Question(topic_id=math_data_handling_topic.id, question_type="multiple_choice",
                                     prompt="What is the mode of 4, 7, 9, 4, 3, 4, 5, 7?", options='["3", "7", "4"]', correct_answer="4").save()
        # Add 25 new questions for 5th Grade Math (Number System and Operations)
        if grade == 5:
            math_ns_ops_topic = Topic(subject_id=math_subject.id, grade=grade, name=f"Math - Grade {grade} Number System and Operations")
            math_ns_ops_topic.save()
            Lesson(topic_id=math_ns_ops_topic.id, title=f"Number System and Operations (Grade {grade})",
                   content="""This lesson covers essential concepts in number systems including LCM, HCF, mean, median, mode, and fundamental operations like multiplication, division, and fractions.""").save()

            # --- Word Problems ---
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="A box contains 12 apples. If you buy 5 boxes, how many apples do you have in total? ____",
                     correct_answer="60").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="John has 24 candies. He shares them equally among 4 friends. How many candies does each friend get?",
                     options='["4", "6", "8", "12"]', correct_answer="6").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="There are 7 days in a week. How many days are there in 8 weeks? ____",
                     correct_answer="56").save()

            # --- LCM and HCF ---
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="What is the LCM of 4 and 6?",
                     options='["2", "12", "24", "1"]', correct_answer="12").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="The HCF of 10 and 15 is ____.",
                     correct_answer="5").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="What is the LCM of 3 and 5?",
                     options='["1", "8", "15", "30"]', correct_answer="15").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="The HCF of 12 and 18 is ____.",
                     correct_answer="6").save()

            # --- Mean, Mode, Median ---
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="Find the mean of: 2, 4, 6, 8.",
                     options='["4", "5", "6", "7"]', correct_answer="5").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="What is the mode of: 1, 2, 2, 3, 4? ____",
                     correct_answer="2").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="Find the median of: 3, 1, 5, 2, 4.",
                     options='["1", "2", "3", "4"]', correct_answer="3").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="The mean of 5, 7, 9 is ____.",
                     correct_answer="7").save()

            # --- Common Multiplication and Division ---
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="What is 7 multiplied by 8? ____",
                     correct_answer="56").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="Divide 45 by 9.",
                     options='["4", "5", "6", "7"]', correct_answer="5").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="What is 12 x 10? ____",
                     correct_answer="120").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="How many times does 7 go into 49?",
                     options='["6", "7", "8", "9"]', correct_answer="7").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="If you have 6 groups of 5, how many do you have in total? ____",
                     correct_answer="30").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="What is 81 divided by 9?",
                     options='["7", "8", "9", "10"]', correct_answer="9").save()

            # --- Fractions ---
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="Which is equivalent to 1/2?",
                     options='["2/3", "2/4", "3/5", "1/4"]', correct_answer="2/4").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="What is 1/4 + 1/4? (in simplest form) ____",
                     correct_answer="1/2").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="Subtract 3/5 from 4/5.",
                     options='["1/5", "2/5", "1/10", "7/5"]', correct_answer="1/5").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="What is 2/3 of 9? ____",
                     correct_answer="6").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="Which fraction is largest: 1/3, 1/2, 1/4?",
                     options='["1/3", "1/2", "1/4"]', correct_answer="1/2").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="Simplify the fraction 6/8. ____",
                     correct_answer="3/4").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="multiple_choice",
                     prompt="If you have 1/2 a pizza and eat 1/4 of it, how much is left?",
                     options='["1/4", "1/2", "3/4", "0"]', correct_answer="1/4").save()
            Question(topic_id=math_ns_ops_topic.id, question_type="fill_in_the_blank",
                     prompt="Convert the mixed number 1 1/2 to an improper fraction. ____",
                     correct_answer="3/2").save()

                # Add spelling test for 5th Grade English (both simple and moderate words)
        if grade == 5:
            english_spelling_topic = Topic(subject_id=english_subject.id, grade=grade, name=f"English - Grade {grade} Spelling Test")
            english_spelling_topic.save()
            Lesson(topic_id=english_spelling_topic.id, title=f"Spelling Practice (Grade {grade})",
                   content="""Practice your spelling skills by filling in the missing letters or choosing the correct spelling.""").save()

            spelling_words = [
                "apple", "table", "chair", "happy", "smile", "dream", "sleep", "write", "listen", "garden",
                "flower", "bright", "friend", "family", "brother", "sister", "always", "clever", "quick", "often",
                "watch", "learn", "school", "study", "pencil", "paper", "book", "story", "music", "dance",
                "paint", "build", "create", "share", "clean", "small", "large", "funny", "quiet", "proud",
                "kind", "heart", "light", "night", "early", "ready", "travel", "happy", "wonder", "magic",
                "picnic", "cookie", "yellow", "purple", "orange", "green", "blue", "brown", "black", "white",
                "seven", "eight", "nine", "ten", # Existing simple words

                "comfortable", "remember", "insertion", "invisible", "beautiful", "challenge", "different", "difficult",
                "discovery", "encourage", "excellent", "fascinate", "favorite", "generous", "governor", "happiness",
                "important", "independent", "information", "interesting", "knowledge", "language", "laughter", "library",
                "magnificent", "mathematics", "medicine", "mountain", "mysterious", "necessary", "neighbor", "nuisance",
                "occasion", "opposite", "original", "parliament", "peculiar", "physical", "pleasure", "position",
                "possible", "practice", "pressure", "privilege", "probably", "question", "receive", "recognize",
                "recommend", "relevant", "restaurant", "schedule", "separate", "sincere", "surprise", "system",
                "through", "tomorrow", "travel", "unusual", "valuable", "various", "vegetable", "village", "weather",
                "wonderful" # New moderate words
            ]
            import random
            for word in spelling_words:
                missing_index = random.randint(0, len(word) - 1)
                prompt_list = list(word)
                prompt_list[missing_index] = '_'
                prompt = f"Fill in the missing letter: {''.join(prompt_list)}"
                Question(topic_id=english_spelling_topic.id, question_type="fill_in_the_blank",
                         prompt=prompt, correct_answer=word).save()

        print("Initial data seeded successfully.")

if __name__ == '__main__':
    seed_initial_data()
