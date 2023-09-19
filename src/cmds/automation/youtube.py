import aiohttp
import asyncio
import discord
import traceback

from discord.ext import commands
from pymongo import MongoClient

from src.config import AutomationVars, SecretVars

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_message = dict()
        self.timer = 864
        self.start = False

    # Used to turn the cog on/off
    @commands.command()
    async def youtube(self, ctx: commands.Context):
        if self.start == False:
            self.start = True
            await ctx.send("Youtube Cog activated!")
            await self.automate()
        else:
            self.start = False
            await ctx.send("Youtube Cog deactivated!")

    # Constructs the embed message to be sent to Discord
    async def construct_data(self, response):
        entry = response['items'][0]
        video_data = {
                '_id': entry['id']['videoId'],
                'title': entry['snippet']['title'],
                'thumbnail': entry['snippet']['thumbnails']['high']['url'],
                'channel': entry['snippet']['channelTitle'],
                'time': entry['snippet']['publishTime']
        }
        self.embed_message.clear()
        self.embed_message = video_data

    # Sends embed_message to channel
    async def on_new_video(self):
        channel = self.bot.get_channel(AutomationVars.DISCORD_CHANNEL)

        author = self.embed_message['channel']

        embed = discord.Embed(
            title=self.embed_message['title'],
            color=discord.Colour.blurple()
        )
        embed.set_author(name=author)
        embed.set_image(url=f'{self.embed_message["thumbnail"]}')
        embed.add_field(name='URL', value=f'https://www.youtube.com/watch?v={self.embed_message["_id"]}')
        embed.set_thumbnail(url='https://i.imgur.com/zwHqAkd.png')

        await channel.send(f"{self.embed_message['channel']} uploaded a new video.", embed=embed)

    # Establishes connection to database to write or discard embed_message
    async def mongo_connection(self):
        post_id = self.embed_message['_id']
        try:
            client = MongoClient(host=SecretVars.MONGO_HOST, port=SecretVars.MONGO_PORT,
                                  username=SecretVars.MONGO_USER, password=SecretVars.MONGO_PASS)
            db = client[SecretVars.MONGO_DATABASE]
            collections = db.list_collection_names()

            if 'youtube' in collections:
                col = db["youtube"]
                document = col.find_one({'_id': post_id})

                if document is not None and document.get('_id') == post_id:
                    print(f"Video already in memory!\nDiscarding Message...")
                    self.embed_message.clear()
                    return
                else:
                    col.insert_one(self.embed_message)
                    print("Video added to database!")
        except Exception as e:
            print(f"ERROR: {e}")
            self.embed_message.clear()
        finally:
            client.close()

    # Fetches the latest video from Genshin Impact Channel
    async def fetch(self, session):
        url = f"https://www.googleapis.com/youtube/v3/search?key={SecretVars.YOUTUBE_API_KEY}"
        url += f"&part={AutomationVars.DATATYPE}"
        url += f"&channelId={AutomationVars.YOUTUBE_CHANNELID}"
        url += f"&maxResults=1&type=video&videoEmbeddable=true&order=date"

        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            return await response.json()

    # Automates get requests every hour to the Youtube API
    async def automate(self):
        while self.start:
            try:
                async with aiohttp.ClientSession() as session:
                    response = await self.fetch(session)
                    await self.construct_data(response)
                    print(f"{self.embed_message}")
                    await self.mongo_connection()

                    # If content exists then perform on_new_video(), otherwise it doesn't send
                    if self.embed_message:
                        await self.on_new_video()

                    await asyncio.sleep(self.timer)
            except Exception as e:
                print(f"ERROR: {e}")
                await asyncio.sleep(self.timer)
                continue