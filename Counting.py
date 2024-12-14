import discord  # type: ignore
from discord.ext import commands  # type: ignore
import os
from pymongo import MongoClient  # type: ignore

mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client[os.getenv('DATABASE_NAME')]
counter_collection = db["counters"]

class CountingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not message.channel or message.channel.id != 1311895191648473118:
            return

        current_count = self.get_count()

        try:
            result = eval(message.content)

            if isinstance(result, (int, float)) and result == current_count + 1:
                self.update_count(result)
                await message.channel.send(f"Correct! The number is now {result}.")
            else:
                self.update_count(0)
                await message.channel.send(f"Oops! The number was reset. The current number is now 0. Try again!")
        except Exception as e:
            pass

    def get_count(self):
        count_data = counter_collection.find_one({"_id": "counting"})
        if count_data:
            return count_data["value"]
        else:
            return 0

    def update_count(self, new_count):
        counter_collection.update_one({"_id": "counting"}, {"$set": {"value": new_count}}, upsert=True)

async def setup(bot):
    await bot.add_cog(CountingCog(bot))
