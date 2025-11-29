import os
import logging
import json
import time # Import time for retries
import google.generativeai as genai

# Setup logging for this module
logger = logging.getLogger(__name__)

class LLMService:
    _model = None
    _MAX_RETRIES = 3 # Define max retries

    @classmethod
    def initialize(cls):
        """Initializes the Gemini API client using the API key from environment variables."""
        api_key = os.getenv("GEMINI_API_KEY")
        print(f"{'Using Gemini API Key from environment variable.{api_key}' if api_key else 'GEMINI_API_KEY not found in environment.'}")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not set.")
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        try:
            genai.configure(api_key=api_key)
            # list avaialble models for debugging
            # available_models = models.list_models()
            # logger.info(f"Available models: {available_models}")
            # # choose the flash or lite model as per requirement
            # for model in available_models:
            #     logger.info(f"Model: {model}")
            cls._model = genai.GenerativeModel('gemini-2.5-flash-lite')
            logger.info("Gemini API client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API client: {e}")
            raise

    @classmethod
    def get_model(cls):
        """Returns the initialized generative model."""
        if cls._model is None:
            cls.initialize() # Attempt to initialize if not already
        return cls._model

    @classmethod
    def generate_question(cls, subject: str, difficulty_band: str, num_questions: int = 1, context_history: dict = None) -> list:
        """
        Generates questions using the LLM based on subject, difficulty, and optional context.
        Returns a list of dictionaries, each representing a question.
        """
        model = cls.get_model()
        if not model:
            raise RuntimeError("LLMService is not initialized.")

        # Extract context variables
        topic = context_history.get("topic", "") if context_history else ""
        additional_instructions = context_history.get("additional_instructions", "") if context_history else ""
        num_options = context_history.get("num_options", 0) if context_history else 0

        prompt_parts = [
            f"Generate {num_questions} {subject} questions suitable for a {difficulty_band} level student. ",
        ]

        if topic:
            prompt_parts.append(f"The questions should be specifically about the topic: {topic}. ")

        prompt_parts.append("Each question should include a question_text, an array of possible_answers (if multiple choice, otherwise empty), the correct_answer, a detailed explanation for the correct answer, the subject, and the difficulty_band. ")
        
        if subject == "English":
            prompt_parts.append(f"For English, we want the user to be quized on grammer, comprehension and vocabulary and spellings at the {difficulty_band} level. ")
        elif subject == "Math":
            prompt_parts.append("For Math, the users are at level of above 5th grade in India, so questions should be tailored accordingly. ")
            if num_options > 0:
                prompt_parts.append(f"Ensure that each question has exactly {num_options} distinct possible answers. ")

        if additional_instructions:
            prompt_parts.append(f"{additional_instructions} ")

        prompt_parts.append("Respond ONLY with a JSON array of question objects. Example format: ")
        prompt_parts.append(
            json.dumps([
                {
                    "question_text": "What is mean and median of the dataset [2, 3, 5, 7, 11]?",
                    "possible_answers": ["Mean: 5.6, Median: 5", "Mean: 4.5, Median: 4", "Mean: 6, Median: 6"],
                    "correct_answer": "Mean: 5.6, Median: 5",
                    "explanation": "The mean is the average of the numbers, calculated as (2+3+5+7+11)/5 = 5.6. The median is the middle value when the numbers are sorted, which is 5.",
                    "subject": "Math",
                    "difficulty_band": "Beginner"
                },
                {
                    "question_text": "What is LCM of 4 and 5?",
                    "possible_answers": ["20", "10", "15"],
                    "correct_answer": "20",
                    "explanation": "The least common multiple (LCM) of 4 and 5 is 20 because 20 is the smallest number that both 4 and 5 divide into without leaving a remainder.",
                    "subject": "Math",
                    "difficulty_band": "Beginner"
                },
                {
                    "question_text": "Identify the nouns and adverbs in the following sentence: 'The quick brown fox jumps swiftly over the lazy dog.'",
                    "possible_answers": ["Nouns: fox, dog; Adverbs: quickly, swiftly", "Nouns: fox, dog; Adverbs: swiftly", "Nouns: quick, brown; Adverbs: jumps"],
                    "correct_answer": "Nouns: fox, dog; Adverbs: quickly, swiftly",
                    "explanation": "Identify Nouns and Adverbs in the sentence.",
                    "subject": "English",
                    "difficulty_band": "Beginner"
                },
                {
                    "question_text": "Show the correct spelling of the following words: accomodate, definately, goverment, recieve, untill.",
                    "possible_answers": ["accommodate, definitely, government, receive, until", "accomodate, definately, goverment, recieve, untill", "acommodate, definately, government, recieve, untill"],
                    "correct_answer": "accommodate, definitely, government, receive, until",
                    "explanation": "Show the correct spelling of the following words: accomodate, definately, goverment, recieve, untill.",
                    "subject": "English",
                    "difficulty_band": "Beginner"
                }
            ])
        ) # Added closing parenthesis for json.dumps and prompt_parts.append

        full_prompt = "".join(prompt_parts)
        logger.info(f"Sending prompt to LLM: {full_prompt[:200]}...") # Log first 200 chars of prompt

        response = None # Initialize response to None
        for attempt in range(cls._MAX_RETRIES):
            try:
                response = model.generate_content(full_prompt)
                # Assuming the response text is directly a JSON string
                response_text = response.text.strip()
                
                # Clean up markdown code block if present
                if response_text.startswith("```json"):
                    response_text = response_text[len("```json"):].strip()
                if response_text.endswith("```"):
                    response_text = response_text[:-len("```")].strip()

                questions_data = json.loads(response_text)
                logger.info(f"Successfully generated {len(questions_data)} questions.")
                return questions_data
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{cls._MAX_RETRIES} - Error generating or parsing questions from LLM: {e}")
                logger.error(f"LLM Response (raw): {getattr(response, 'text', 'N/A')}")
                if attempt < cls._MAX_RETRIES - 1:
                    time.sleep(2) # Wait before retrying
                else:
                    raise # Re-raise the exception after all retries are exhausted

if __name__ == '__main__':
    # This block is for testing purposes only
    # In a real application, setup_logging would be called once at startup
    from services.logging_service import setup_logging
    setup_logging()

    # Set a dummy API key for testing this module's initialization
    # In a real scenario, this would be set in the environment
    # os.environ["GEMINI_API_KEY"] = "YOUR_DUMMY_API_KEY" 
    
    try:
        llm_client = LLMService.get_model()
        print("LLM client obtained successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
