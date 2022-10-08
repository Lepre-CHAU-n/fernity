import discord
import requests
from discord.ext import commands

class Fun(discord.Cog):
    def init(self, bot):
        self.bot = bot

    @discord.slash_command(description = "It shows you a cat gif")
    async def catgif(self,ctx):
        catGif = requests.get('http://thecatapi.com/api/images/get?format=src&type=gif')
        try:
            embed = discord.Embed(
                title="Cat Gif", 
                description=f"Here's a random cat gif!",
                color=ctx.author.color)
            catGif = catGif.url
            embed.set_image(url=catGif)
            await ctx.respond(embed=embed)
        except:
            await ctx.respond('Error 404. Website may be down.')

    
    @discord.slash_command(name="avatar", description="Retrives an avatar.") 
    async def avatar(self,ctx, member: discord.Member):
        embed = discord.Embed(
            title="Avatar", 
            description=f"Here's your enlarged avatar, {member.name}!",
            color=ctx.author.color)
        embed.set_image(url=member.display_avatar.url)
        await ctx.respond(embed=embed)
  
def setup(bot):
    bot.add_cog(Fun(bot))