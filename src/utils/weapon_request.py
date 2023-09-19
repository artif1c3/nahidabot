import aiohttp
import asyncio
import json


class WeaponRequest:
    def __init__(self):
        self.w_queries = []
        self.w_prompt_extension = {}

    # Constructs the prompt to be sent
    def construct_prompt(self, weapon):
        self.w_prompt_extension.clear() # Clears the previous prompt_extension -- If you don't do this, it keep the previous prompt!
        key = weapon['name']
        self.w_prompt_extension.setdefault(key, []).append(weapon)
        print(self.w_prompt_extension)

    # Constructs the data to build the prompt
    def construct_data(self, response):
        weapon = {
            'name': response.get('name'),
            'substat': response.get('substat'),
            'weaponmaterial': response.get('weaponmaterialtype'),
            'costs': response.get('costs'),
        }
        return weapon

    # Fetches data from the genshindb API
    async def fetch(self, session, query):
        query = query.replace(" ", "").lower().strip()
        async with session.get(f"https://genshin-db-api.vercel.app/api/weapons?query={query}") as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.text()

    # Creates tasks to complete and fetch data
    async def fetch_all(self, session):
        tasks = []
        for query in self.w_queries:
            task = asyncio.create_task(self.fetch(session, query))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

    async def main(self):
        async with aiohttp.ClientSession() as session:
            responses = await self.fetch_all(session)
            for response in responses:
                response = json.loads(response)
                weapon = self.construct_data(response)
                self.construct_prompt(weapon)

async def run_weapon_request():
    weapon_request = WeaponRequest()
    await weapon_request.main()

asyncio.run(run_weapon_request())