import os
import logging
import json
import google.generativeai as genai

# Setup logging for this module
logger = logging.getLogger(__name__)

class LLMService:
    _model = None

    @classmethod
    def initialize(cls):
        """Initializes the Gemini API client using the API key from environment variables."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not set.")
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        try:
            genai.configure(api_key=api_key)
            cls._model = genai.GenerativeModel('gemini-pro')
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
    def generate_question(cls, subject: str, difficulty_band: str, num_questions: int = 1, context_history: str = None) -> list:
        """
        Generates questions using the LLM based on subject, difficulty, and optional context.
        Returns a list of dictionaries, each representing a question.
        """
        model = cls.get_model()
        if not model:
            raise RuntimeError("LLMService is not initialized.")

        prompt_parts = [
            f"Generate {num_questions} {subject} questions suitable for a {difficulty_band} level student. ",
            "Each question should include a question_text, an array of possible_answers (if multiple choice, otherwise empty), the correct_answer, a detailed explanation for the correct answer, the subject, and the difficulty_band. "
            "Respond ONLY with a JSON array of question objects. Example format: ",
            json.dumps([
                {
                    "question_text": "What is 2 + 2?",
                    "possible_answers": ["3", "4", "5"],
                    "correct_answer": "4",
                    "explanation": "2 + 2 equals 4. It is a basic arithmetic operation.",
                    "subject": "Math",
                    "difficulty_band": "Beginner"
                }
            ])
        ]
        
        if context_history:
            prompt_parts.append(f"Consider the student's performance history: {context_history}. Adapt questions accordingly.")

        full_prompt = "".join(prompt_parts)
        logger.info(f"Sending prompt to LLM: {full_prompt[:200]}...") # Log first 200 chars of prompt

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
            logger.error(f"Error generating or parsing questions from LLM: {e}")
            logger.error(f"LLM Response (raw): {getattr(response, 'text', 'N/A')}")
            raise

if __name__ == '__main__':
    # This block is for testing purposes only
    # In a real application, setup_logging would be called once at startup
    from services.logging_service import setup_logging
    setup_logging()

    # Set a dummy API key for testing this module's initialization
    # In a real scenario, this would be set in the environment
    os.environ["GEMINI_API_KEY"] = "YOUR_DUMMY_API_KEY" 
    
    try:
        llm_client = LLMService.get_model()
        print("LLM client obtained successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Clean up dummy key
    del os.environ["GEMINI_API_KEY"]
