# from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv
import os
from anthropic import Anthropic
import json


class GameConfigurationSightWords:
    def __init__(self):
        # Instance attributes (can vary per game)
        self.target_group = "adults (20-50 years old) struggling with reading and having basic vocabulary and comprehension abilities"
        self.model = "claude-3-5-sonnet-20241022"
        self.system_prompt = """You are an educational expert specializing in UK phonics and reading instruction for adult learners. """
        self.response_format = """
        {
        "questions": [
            {
            "question_id": "[1]",
            "question_type": "gap-fill-sight-words",
            "context": "[context category]",
            "sight_words": ["word", "word"]
            "question_text": "[sentence with ______ gaps]",
            "gaps": 2,
            "options": ["option", "option"],
            "correct_order": ["option", "option"]
            }
        ]
        }
        """

        self.example = """
        {
          "questions": [
            {
            "question_id": "1",
            "question_type": "gap-fill",
            "context": "Daily Activities",
            "sight_words": "one, work",
            "question_text": "______ day I will ______ in a shop of my own but this is fine for me now",
            "gaps": 2,
            "options": ["work", "one"],
            "correct_order": ["one", "work"]
            }
        ]
        }"""


class GapFillGeneratorSightWords:
    """Class to handle gap fill exercise generation"""
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = GameConfigurationSightWords()
        self.sent_nbr = 2
        
    def build_prompt(self, focus_sight_words: str) -> str:
        return f"""
        Your task is to create engaging gap-fill sentences focusing on specific sight words.
        Please carefully read the following information and instructions before proceeding.        
        <list of sight words>
        {focus_sight_words}
        </list of sight words>
        
        TARGET AUDIENCE: 
        - {self.config.target_group}
        EDICATIONAL GOALS:
        - Reinforce sight words pronunciation 
        - Develop contextual understanding
        
        INSTRUCTIONS:
        1. Generate this number of sentences {self.sent_nbr}, each containing 2 gaps (indicated by a full underscore line: _____)
        2. Each sentence must:
            - be clear and practical
            - include sufficient context clues for comprehension
            - contain 15-30 words
            - be grammatically correct and natural-sounding
        3. Focus on the specified sight words, ensuring that the gaps correspond to words exemplifying these patterns.
        4. Present options in random order
        5. Return response in this exact JSON structure:
        <JSON structure>
        {self.config.response_format}
        </JSON structure>

        EXAMPLE OF ONE QUESTION:
        <example>
        {self.config.example}
        </example>

        QUALITY CHECKS:
        - Ensure readability at basic level
        - Verify natural flow of text
        - Confirm appropriate context clues
        - Check the response, only JSON file.
        """
    def generate_exercises(self, focus_sight_words: str) -> Dict:
        prompt = self.build_prompt(focus_sight_words)
        # print(prompt)
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=2000,
            system=self.config.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        result = response.content[0].text
        # result_json = json.loads(result)
        return result

def main():
    sight_words_list = [
        "so",
        "work",
        "love",
        "their",
        "one",
        "over",
        "sure",
        "two",
        "knew",
        "because",
        "only",
        "woman",
        "done",
        "does",
        "other"
    ]
    sight_words_list_str = ''.join(sight_words_list)
    # Create the full focus_sight_words
    focus_sight_words = f"""Please focus on these sight words:\n"
        {sight_words_list_str}"""

    # Initialize the generator
    generator = GapFillGeneratorSightWords()

    # # Generate exercises
    result = generator.generate_exercises(focus_sight_words)
    print(result)

    result_json = json.loads(result)

    with open('game3_sight_words_questions.json', 'w') as json_file:
        json.dump(result_json, json_file, indent=4)
    
    return result_json

if __name__ == "__main__":
    main()