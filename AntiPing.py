import discord # type: ignore
from discord.ext import commands # type: ignore

class AntiPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_ids = [1311894909825056808, 1311894904737370195, 1311894903135014962, 1311894900966690889, 1311894898437259286]
        self.role_ids_immune = [1311894909825056808, 1311894904737370195, 1311894903135014962, 1311894900966690889, 1311894898437259286, 1311894919572357190, 1311894931383648256, 1315159343276097587, 1311894959099740214, 1311894983787286579, 1311894897825153044]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        for mentioned_user in message.mentions:
            member = message.guild.get_member(mentioned_user.id)
            if member is not None:
                if any(role.id in self.role_ids for role in member.roles):
                    if any(role.id in self.role_ids_immune for role in message.author.roles):
                        return
                    else:
                        await message.reply("You may not mention users of our ownership team.")
                        return

    
async def setup(bot):
  await bot.add_cog(AntiPing(bot))