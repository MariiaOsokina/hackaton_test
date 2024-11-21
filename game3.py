from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv
import os
from anthropic import Anthropic

class GameConfiguration:
    def __init__(self):
        # Instance attributes (can vary per game)
        self.target_group = "adults (20-50 years) struggling with reading and having basic vocabulary and comprehension abilities"
        self.paragr_nbr = 2
        self.model = "claude-3-5-sonnet-20241022"
        self.system_prompt = """You are an educational expert specialising in UK phonics and reading instruction for adult learners."""
        self.response_format = """
        {
          "questions": [
            {
              "question_id": "1",
              "question_type": "gap-fill",
              "context": "[context category]",
              "phonics/sight words": "[sound pattern]",
              "pattern": "[spelling pattern]",
              "question_text": "[paragraph with ______ gaps]",
              "gaps": 2,
              "options": ["option", "option"],
              "correct_order": ["option", "option"]
            }
          ]
        }"""
        self.example = """
        {
        "question_id": "2",
        "question_type": "gap-fill",
        "context": "Weather",
        "phonics": "'ow' sound and 'er' sound",
        "pattern": "ow, er",
        "question_text": "Dark clouds brought a heavy _____. The _____ report says it will clear up soon.",
        "gaps": 2,
        "options": ["shower", "weather"],
        "correct_order": ["shower", "weather"]
        },"""

class GapFillGenerator:
    """Class to handle gap fill exercise generation"""
    def __init__(self):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = GameConfiguration()
        
    def build_prompt(self, focus_topic: str) -> str:
        return f"""
        Create a set of engaging gap-fill paragraphs following these instructions:
        <focus topic>
        Please do proper analysis of phonics and focus on these phonics patterns:
        {focus_topic}
        </focus topic>
        
        LEARNING GOALS:
        - Reinforce phonics patterns
        - Develop contextual understanding
        - Target audience: {self.config.target_group}
        
        GUIDELINES:
        - Generate {self.config.paragr_nbr} paragraphs, each containing 2 gaps
        - Paragraph must be clear and practical
        - Include sufficient context clues for comprehension
        - Maximum word count per paragraph: 25-40 words
        
        OUTPUT FORMAT:
        - Use complete word gaps (indicated by a full underscore line: _____)
        - Return response in this EXACT JSON structure:
        <JSON structure>
        {self.config.response_format}
        </JSON structure>

        EXAMPLE OF GOOD RESPONSE:
        <example>
        {self.config.example}
        </example>

        ADDITIONAL REQUIREMENTS:
        - Present options in random order
        - If using multiple phonics patterns, list all patterns used
        - Ensure all  sentences are grammatically correct and natural-sounding

        QUALITY CHECKS:
        - Ensure readability at basic level
        - Verify natural flow of text
        - Confirm appropriate context clues
        - Check the response, only JSON file.
        """

    def generate_exercises(self, focus_topic: str) -> Dict:
        prompt = self.build_prompt(focus_topic)
        print(prompt)
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=2000,
            system=self.config.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text

def main():
    # Initialize the generator
    generator = GapFillGenerator()
    
    # Define your focus topic
    focus_topic1 = """
    - the [er] sound in the form of the [e-r], [i-r] or [u-r] letter combination(patterns). Some examples for better understanding the patterns: [...] """
    focus_topic2 = """
    - the [(Long) ō"] sound in the form of the [oa] or [ow] letter combination(patterns). Some examples for better understanding the patterns: [...] """
    """
    focus_topic3 = """
        "sound": "(Long) ū",
        "pattern": "u_e",
        },"""
    
    focus_topic4 = f"""- the ["zh"] sound in the form of the "si" letter combination(patterns). Some examples for better understanding the patterns: ["television"] """
"""

    focus_topic5 = """
    "sound_w": {
    "sound": "w",
    "patterns": [
        {
        "pattern": "wh",

        }
    ]
    },
    "sound_x": {
    "sound": "x (ks)",
    "patterns": [
        {
        "pattern": "x",
        }
    ]"""
    
    focus_topic6 = """
"long_a_sounds": {
    "sound": "(Long) ā",
    "patterns": [
        {
        "pattern": "ai",
        "level": 2,
        "description": "vowel digraph",
        "examples": ["rain"]
        },
        {
        "pattern": "ay",
        "level": 2,
        "description": "vowel digraph",
        "examples": ["day"]
        },
        {
        "pattern": "a_e",
        "level": 3,
        "description": "split digraph",
        "examples": ["made", "tape", "male", "pane", "same", "rate", "lake", "bake", "gate", "scrape"]
        },
"""
    # Generate exercises
    result = generator.generate_exercises(focus_topic6)
    print(result)

if __name__ == "__main__":
    main()