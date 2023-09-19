from os import path

from . import character_request as cr
from . import weapon_request as wr

class AiUtils:
    """ 
        Ai utilities that interacts with files in filters
        Filters prompts from the user and used to create requests to genshindb API
    """

    resources_path = path.join(path.dirname(path.abspath(__file__)), 'filters')

    def __init__(self):
        self.character_request = cr.CharacterRequest()
        self.weapon_request = wr.WeaponRequest()
        self.keyword_path = path.join(AiUtils.resources_path, 'keywords.txt')
        self.character_path = path.join(AiUtils.resources_path, 'characters.txt')
        self.weapon_path = path.join(AiUtils.resources_path, 'weapons.txt')

    def get_keywords(self):
        with open(self.keyword_path, 'r') as f:
            keywords = f.read().splitlines()
        
        return keywords
    
    def get_characters(self):
        with open(self.character_path, 'r') as c:
            characters = c.read().splitlines()

        return characters
    
    def get_weapons(self):
        with open(self.weapon_path, 'r') as w:
            weapons = w.read().splitlines()

        return weapons

    # Parses the prompt for characters
    def parse_character(self, prompt):
        characters = self.get_characters()
        prompt_lower = prompt.lower()

        existing_characters = []
        
        for character in characters:
            if character.lower() in prompt_lower:
                existing_characters.append(character.lower())

        return existing_characters
    
    # Parses the prompt for weapons
    def parse_weapon(self, prompt):
        weapons = self.get_weapons()
        prompt_lower = prompt.lower()

        existing_weapons = []

        for weapon in weapons:
            if weapon.lower() in prompt_lower:
                existing_weapons.append(weapon.lower())

        return existing_weapons

    # Requests to the genshindb API 
    async def main(self, prompt):
        existing_characters = self.parse_character(prompt)
        existing_weapons = self.parse_weapon(prompt)

        self.character_request.queries = existing_characters
        self.weapon_request.w_queries = existing_weapons

        await self.character_request.main()
        await self.weapon_request.main()

        prompt_extension = str(self.character_request.prompt_extension)
        prompt_extension += str(f'\n{self.weapon_request.w_prompt_extension}')

        return prompt_extension