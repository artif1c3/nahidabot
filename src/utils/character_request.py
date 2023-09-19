import aiohttp
import asyncio
import json


class CharacterRequest:
    def __init__(self):
        self.queries = []
        self.prompt_extension = {}

    # Constructs the prompt to be sent
    def construct_prompt(self, character):
        self.prompt_extension.clear() # Clears the previous prompt_extension -- If you don't do this, it keep the previous prompt!
        key = character['name']
        self.prompt_extension.setdefault(key, []).append(character)
        print(self.prompt_extension)

    # Constructs the data to build the prompt
    def construct_data(self, response):
        character = {
            'name': response.get('name'),
            'description': response.get('description'),
            'birthday': response.get('birthday'),
            'materials': response.get('costs'),
        }
        return character

    # Fetches data from the genshindb API
    async def fetch(self, session, query):
        query = query.replace(" ", "").lower().strip()
        async with session.get(f"https://genshin-db-api.vercel.app/api/characters?query={query}") as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.text()

    # Creates tasks to complete and fetch data
    async def fetch_all(self, session):
        tasks = []
        for query in self.queries:
            task = asyncio.create_task(self.fetch(session, query))
            tasks.append(task)
        responses = await asyncio.gather(*tasks) # Creates a list of awaitables because of *, unpacks iterables
        return responses

    async def main(self):
        async with aiohttp.ClientSession() as session:
            responses = await self.fetch_all(session)
            for response in responses:
                response = json.loads(response)
                character = self.construct_data(response)
                self.construct_prompt(character)

async def run_character_request():
    character_request = CharacterRequest()
    await character_request.main()

asyncio.run(run_character_request())