import discord
from discord.ext import commands

class Interaction(discord.Cog):
    def init(self, bot):
        self.bot = bot

    @discord.slash_command(name = "hello", description = "Say hello")
    async def hello(self, ctx):
        await ctx.respond("Hey!")
        
    @discord.slash_command(name="deathhug", description="Death hug someone >:)") 
    @commands.cooldown(1, 30, commands.BucketType.user) 
    async def deathhug(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.respond(f"{ctx.author.name} just death hugged {member.mention}! >:)")

    @discord.slash_command(name="hug", description="Hug someone :)") 
    @commands.cooldown(1, 30, commands.BucketType.user) 
    async def hug(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.respond(f"{ctx.author.name} just hugged {member.mention}! Awww.")

    @discord.slash_command(name="kiss", description="Kiss someone <3") 
    @commands.cooldown(1, 30, commands.BucketType.user) 
    async def kiss(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.respond(f"{ctx.author.name} just kissed {member.mention}! <3")
  
    @discord.slash_command(name="pat", description="Pat someone c:")
    @commands.cooldown(1, 30, commands.BucketType.user)  
    async def pat(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.respond(f"{ctx.author.name} just patted {member.mention}! c:")

    @discord.slash_command(name="boop", description="Boop someone :3") 
    @commands.cooldown(1, 30, commands.BucketType.user) 
    async def boop(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.respond(f"{ctx.author.name} just booped {member.mention}! :3")
    


def setup(bot):
    bot.add_cog(Interaction(bot))