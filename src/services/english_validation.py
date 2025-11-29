import re

class EnglishValidationService:
    def __init__(self):
        # Basic common spelling mistakes for demonstration
        self.common_spelling_mistakes = {
            "raning": "raining",
            "beleive": "believe",
            "recieve": "receive",
            "neccessary": "necessary"
        }
        # Basic grammar rules for demonstration (subject-verb agreement for 'to be' verb)
        self.basic_grammar_rules = [
            # Pattern: "It are" -> "It is"
            {"pattern": r"\bIt\s+are\b", "correction": "It is", "error": "Subject-verb agreement error."},
            # Pattern: "They is" -> "They are"
            {"pattern": r"\b(They|We|You)\s+is\b", "correction": r"\1 are", "error": "Subject-verb agreement error."},
            # Pattern: "I are" -> "I am"
            {"pattern": r"\bI\s+are\b", "correction": "I am", "error": "Subject-verb agreement error."},
            # Basic punctuation check (missing period at end)
            {"pattern": r"([^.?!])$", "correction": r"\1.", "error": "Missing punctuation at the end."},
            {"pattern": r"([.?!])([a-z])", "correction": r"\1 \u2022 \u2022 \u2022\2", "error": "Sentence does not start with a capital letter."}
        ]

    def validate_sentence(self, sentence):
        feedback = []
        corrected_sentence = sentence

        # 1. Spelling Check
        words = re.findall(r'\b\w+\b', corrected_sentence.lower())
        for word in words:
            if word in self.common_spelling_mistakes:
                feedback.append(f"Spelling error: '{word}' should be '{self.common_spelling_mistakes[word]}'.")
                corrected_sentence = re.sub(r"\b" + re.escape(word) + r"\b", self.common_spelling_mistakes[word], corrected_sentence, flags=re.IGNORECASE)

        # 2. Basic Grammar Check
        # for rule in self.basic_grammar_rules:
        #     if re.search(rule["pattern"], corrected_sentence):
        #         feedback.append(rule["error"])
        #         # Apply correction for demonstration, but real corrections would be more complex
        #         if "correction" in rule:
        #             corrected_sentence = re.sub(rule["pattern"], rule["correction"], corrected_sentence)

        # # 3. Capitalization check (start of sentence)
        # if corrected_sentence and not corrected_sentence[0].isupper() and not corrected_sentence[0].isnumeric():
        #     feedback.append("Sentence should start with a capital letter.")
        #     corrected_sentence = corrected_sentence[0].upper() + corrected_sentence[1:]

        is_correct = not feedback # If no feedback, then it's correct based on these rules
        return is_correct, feedback, corrected_sentence

if __name__ == '__main__':
    validator = EnglishValidationService()

    # Test cases
    print("--- Test 1: Simple Correct ---")
    sentence1 = "The cat is sleeping."
    correct1, fb1, cs1 = validator.validate_sentence(sentence1)
    print(f"Original: '{sentence1}'\nCorrect: {correct1}\nFeedback: {fb1}\nCorrected: '{cs1}'\n")

    print("--- Test 2: Spelling Error ---")
    sentence2 = "The dog is raning."
    correct2, fb2, cs2 = validator.validate_sentence(sentence2)
    print(f"Original: '{sentence2}'\nCorrect: {correct2}\nFeedback: {fb2}\nCorrected: '{cs2}'\n")

    print("--- Test 3: Grammar Error ---")
    sentence3 = "It are raining heavily."
    correct3, fb3, cs3 = validator.validate_sentence(sentence3)
    print(f"Original: '{sentence3}'\nCorrect: {correct3}\nFeedback: {fb3}\nCorrected: '{cs3}'\n")

    print("--- Test 4: Missing Punctuation ---")
    sentence4 = "The bird sings"
    correct4, fb4, cs4 = validator.validate_sentence(sentence4)
    print(f"Original: '{sentence4}'\nCorrect: {correct4}\nFeedback: {fb4}\nCorrected: '{cs4}'\n")

    print("--- Test 5: All errors ---")
    sentence5 = "it are raning"
    correct5, fb5, cs5 = validator.validate_sentence(sentence5)
    print(f"Original: '{sentence5}'\nCorrect: {correct5}\nFeedback: {fb5}\nCorrected: '{cs5}'\n")
