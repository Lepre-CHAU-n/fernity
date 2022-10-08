from discord.commands import SlashCommandGroup
import discord
from discord.ext import commands, pages


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(title="Help Page",description="**Common Commands**",color=discord.Colour.blurple()),
            discord.Embed(title="Help Page",description="**Interaction Commands**",color=discord.Colour.blurple()),
            discord.Embed(title="Help Page",description="**Mod Commands**",color=discord.Colour.blurple()),
            discord.Embed(title="Help Page",description="**Math and Probability Commands**",color=discord.Colour.blurple()),
        ]
        self.pages[0].add_field(
           name="About", value=f"Fernity's about page",inline=True
        )
        self.pages[0].add_field(
            name="Help", value=f"You are already here",inline=True
        )
        self.pages[0].add_field(
           name="Avatar", value=f"Retrives an avatar",inline=True
        )
        self.pages[0].add_field(
           name="Ping", value=f"Sends the bot's latency",inline=True
        )
        self.pages[0].add_field(
           name="Catgif", value=f"It shows you a cat gif",inline=True
        )
        self.pages[0].add_field(
           name="Speak", value=f"Let bot message for you on channel",inline=True
        )
        self.pages[0].set_footer(text="Fernity - Created on Aug 19, 2022") 


        self.pages[1].add_field(
           name = "Hello", value = "Say hello" ,inline=True
        )
        self.pages[1].add_field(
           name="Deathhug", value = "Death hug someone >:)",inline=True
        )
        self.pages[1].add_field(
           name="Hug", value = "Hug someone :)",inline=True
        )
        self.pages[1].add_field(
           name="Kiss", value = "Kiss someone <3",inline=True
        )
        self.pages[1].add_field(
           name="Pat", value = "Pat someone c:",inline=True
        )
        self.pages[1].add_field(
           name="Boop", value = "Boop someone :3",inline=True
        )
        self.pages[1].set_footer(text="Fernity - Created on Aug 19, 2022") 


        self.pages[2].add_field(
           name="Clear", value=f"Clear messages",inline=True
        )
        self.pages[2].add_field(
           name="Kick", value=f"Kick members",inline=True
        )
        self.pages[2].add_field(
           name="Ban", value=f"Ban members",inline=True
        )
        self.pages[2].add_field(
           name = "Unban", value=f"Unbans a member",inline=True
        )
        self.pages[2].add_field(
           name = 'Timeout', value=f"Mutes/timeouts a member",inline=True
        )
        self.pages[2].add_field(
           name = 'Unmute', value=f"Unmutes/untimeouts a member",inline=True
        )
        self.pages[2].add_field(
           name="Secret", value=f"A private command...",inline=True
        )
        self.pages[2].add_field(
           name="Addrole", value="Add roles to a member",inline=True
        )
        self.pages[2].set_footer(text="Fernity - Created on Aug 19, 2022") 


        self.pages[3].add_field(
           name="Evaluate", value=f"Calculates arithmetic",inline=True
        )
        self.pages[3].add_field(
           name="Root", value=f"Find nth root of number",inline=True
        )
        self.pages[3].add_field(
           name="Dicetoss", value=f"Roll dice",inline=True
        )
        self.pages[3].add_field(
           name="Cointoss", value=f"Toss coin",inline=True
        )
        self.pages[3].set_footer(text="Fernity - Created on Aug 19, 2022") 

    def get_pages(self):
        return self.pages

    @discord.slash_command(name="help")
    async def help(self, ctx: discord.ApplicationContext):
        """Fernity's help page"""
        page_buttons = [
            pages.PaginatorButton(
                "first", emoji="⏪", style=discord.ButtonStyle.blurple
            ),
            pages.PaginatorButton("prev", emoji="⬅", style=discord.ButtonStyle.blurple),
            pages.PaginatorButton(
                "page_indicator", style=discord.ButtonStyle.gray, disabled=True
            ),
            pages.PaginatorButton("next", emoji="➡", style=discord.ButtonStyle.blurple),
            pages.PaginatorButton("last", emoji="⏩", style=discord.ButtonStyle.blurple),
        ]
        paginator = pages.Paginator(
            pages=self.get_pages(),
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=page_buttons,
            loop_pages=True,
        )
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Help(bot))