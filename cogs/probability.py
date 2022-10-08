import discord
import random


class Probability(discord.Cog):
    def init(self, bot):
        self.bot = bot

    @discord.slash_command(name="dicetoss") # creates a prefixed command
    async def gamble(self, ctx): # all methods now must have both self and ctx parameters
        await ctx.respond(random.randint(1, 6))

    @discord.slash_command(name="cointoss") # creates a prefixed command
    async def cointoss(self, ctx): # all methods now must have both self and ctx parameters
        if random.randint(0,1) == 1:
            await ctx.respond("Heads")
        else:
            await ctx.respond("Tails")


def setup(bot):
    bot.add_cog(Probability(bot))