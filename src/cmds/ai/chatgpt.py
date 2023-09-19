import openai

from discord.ext import commands

from src.utils.ai_utils import *

class Ai(commands.Cog):
    """
        Used to get responses from Openai API
    """

    def __init__(self, bot):
        self.bot = bot
        self.utils = AiUtils()

    @commands.command(aliases=['chat', 'gpt'])
    async def ai(self, ctx: commands.Context, *, prompt: str):
        # Creates the prompt extension if a keyword was found from characters.txt or weapons.txt
        prompt_extension = await self.utils.main(prompt) # Was previously run_request()
        extended_prompt = f"{prompt_extension}\n\n{prompt}"
        response = self.get_ai_response(extended_prompt)
        await ctx.send(response)

    # Used to get the AI response from the OpenAI API
    def get_ai_response(self, prompt):
        # Uses gpt 3.5 turbo as the base.
        # For prices on Ai usage refer to OpenAi's price at openai.com/pricing
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[  
                        {
                            "role": "system", 
                            "content": "Your name is Nahida, the god of wisdom and archon of Sumeru. You are a chatbot assistant that helps answer questions about Genshin Impact."
                        },
                        {
                             "role": "system",
                             "content": "If you have any questions please send Artif1c3 a DM on Discord, his Discord ID is #Artifice1547."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                         },
                         ],
            temperature = 1,
            max_tokens = 1000,
            stream = True,
        )

        # Constructs the message from Openai API
        message = ""
        words = list()
        for word in response:
            try:
                words.append(word["choices"][0]["delta"]["content"])
                message = "".join(words)
            except:
                pass

        return message