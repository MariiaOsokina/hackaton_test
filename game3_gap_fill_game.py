# from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv
import os
from anthropic import Anthropic
import json


class GameConfiguration:
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
            "question_type": "gap-fill",
            "context": "[context category]",
            "phonics": "[sound pattern]",
            "pattern": "[spelling pattern]",
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
            "phonics": "long 'a' sound",
            "pattern": "a_e, ai",
            "question_text": "Every morning, I _____ breakfast at eight. The _____ was falling as I walked to work.",
            "gaps": 2,
            "options": ["rain", "make"],
            "correct_order": ["make", "rain"]
            }
        ]
        }"""


class GapFillGenerator:
    """Class to handle gap fill exercise generation"""
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = GameConfiguration()
        self.sent_nbr = 2
        
    def build_prompt(self, focus_phonics: str) -> str:
        return f"""
        Your task is to create engaging gap-fill sentences focusing on specific phonics patterns.
        Please carefully read the following information and instructions before proceeding.        
        <focus phonics>
        {focus_phonics}
        </focus pohonics>
        
        TARGET AUDIENCE: 
        - {self.config.target_group}
        EDICATIONAL GOALS:
        - Reinforce phonics patterns
        - Develop contextual understanding
        
        INSTRUCTIONS:
        1. Generate this number of sentences {self.sent_nbr}, each containing 2 gaps (indicated by a full underscore line: _____)
        2. Each sentence must:
            - be clear and practical
            - include sufficient context clues for comprehension
            - contain 15-30 words
            - be grammatically correct and natural-sounding
        3. Focus on the specified phonics patterns, ensuring that the gaps correspond to words exemplifying these patterns.
        4. Present options in random order
        5. If using multiple phonics patterns, list all patterns used
        6. Return response in this exact JSON structure:
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
    def generate_exercises(self, focus_phonics: str) -> Dict:
        prompt = self.build_prompt(focus_phonics)
        # print(prompt)
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=2000,
            system=self.config.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # print (response.usage)
        return response.content[0].text


def main():
    patterns = [
        {
            'sound': 'er',
            'pattern': 'er',
            'examples': ["her", "term", "bitter", "herb", "infer", "better", "chatter", "verb", "sister", "faster", "transfer", "stern"]
        },
        {
            'sound': 'er',
            'pattern': 'ur',
            'examples': ["burn", "hurt", "church", "blur", "curl", "fur", "furnish", "Thursday", "turn", "slur", "surf", "burst"]
        },
        {
            'sound': 'er',
            'pattern': 'ir',
            'examples': ["first", "dirt", "skirt", "sir", "bird", "girl", "birthday", "thirty", "stir", "third", "firm", "birth"]
        }
    ]

    # Create the full focus_phonics
    focus_phonics = "Please do proper analysis of phonics and focus on these phonics patterns:\n"
    for pattern in patterns:
        focus_phonics += f"""
        - the '{pattern['sound']}' sound in the form of the '{pattern['pattern']}' patterns (letter combinations), "examples": {pattern['examples']}"""
    
    # Initialize the generator
    generator = GapFillGenerator()

    # # Generate exercises
    result = generator.generate_exercises(focus_phonics)
    print(result)

    result_json = json.loads(result)

    with open('game3_questions.json', 'w') as json_file:
        json.dump(result_json, json_file, indent=4)
    
    return result_json

if __name__ == "__main__":
    main()