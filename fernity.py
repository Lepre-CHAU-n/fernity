
import discord
from discord import Option
from datetime import timedelta
import os # default module
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import tasks, commands
import asyncio
import re
from dotenv import load_dotenv
load_dotenv() # load all the variables from the env file
intents=discord.Intents.all()
intents.messages = True
intents.members = True
DEV_ID = os.environ.get("DEV_ID")
BOT_ID = os.environ.get("BOT_ID")
bot = discord.Bot(intents=intents,owner_id = int(DEV_ID))


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    change_status.start() #to start the looping task
 

@tasks.loop()
async def change_status():
  await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,name="over 10+ servers"))
  await asyncio.sleep(300)
  await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="type /help"))
  await asyncio.sleep(300)
  await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("AUUGHHH"))
  await asyncio.sleep(300)


@bot.event
async def on_member_join(member):
    await member.send(
        f'Welcome to the server, {member.mention}! Enjoy your stay here.'
    )

@bot.slash_command(description="Sends the bot's latency.") # this decorator makes a slash command
@commands.cooldown(1, 10, commands.BucketType.user) 
async def ping( ctx : discord.ApplicationContext): # a slash command will be created with the name "ping"
  embed = discord.Embed(
    title="Pong!", 
    description=f':ping_pong: Latency is: {round(bot.latency * 1000)} ms'
    ) 
  await ctx.respond(embed=embed)


@bot.command(pass_context=True,description="Clear messages")
@has_permissions(moderate_members = True)
async def clean(ctx, limit: int):
  if limit > 100:
    await ctx.response.send_message(f'Sorry, you cannot clear more than 100 messages')
  else:
    await ctx.channel.purge(limit=limit)
    await ctx.response.send_message(f'{limit} cleared by {ctx.author.name}',ephemeral=True)
@clean.error
async def clean_error(ctx, error):
  if clean(error,MissingPermissions):
    await ctx.respond("You do not have required permission for the action performed")
  else:
    raise error  # Here we raise other errors to ensure they aren't ignored


@bot.command(description="Kick members")
@has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, description = "The User ID of the person you want to ban.", required = True),*,reason=None):
  if member.id == ctx.author.id: #checks to see if they're the same
    await ctx.respond("You can't kick yourself!")
  else:
    try:
      await member.send(f'The user {member} has been kicked from the server. Reason: {reason}')
      await ctx.respond(f"Message has been sent!", ephemeral = True)
      await ctx.respond(f'The user {member} has been kicked from the server. Reason: {reason}')
    except:
      await member.kick(reason=reason)
      await ctx.respond(f"Message has not been sent. It seems like this user turned off dms.",ephemeral = True)
      await ctx.respond(f'The user {member} has been kicked from the server. Reason: {reason}')
async def kick_error(ctx,error):
  if kick(error,MissingPermissions):
    await ctx.respond("You do not have required permission for the action performed")
  else:
    raise error  # Here we raise other errors to ensure they aren't ignored


@bot.command(description="Ban members")
@has_permissions(ban_members=True)
async def ban(ctx,member: Option(discord.Member, description = "The User ID of the person you want to ban.", required = True),*,reason=None):
  if member.id == ctx.author.id: #checks to see if they're the same
    await ctx.respond("You can't ban yourself!")
  else:
    try:
      await member.send(f'The user {member} has been banned from the server. Reason: {reason}')
      await ctx.respond(f"Message has been sent!", ephemeral = True)
      await ctx.respond(f'The user {member} has been banned from the server. Reason: {reason}')
    except:
      await member.ban(reason=reason, clean = clean)
      await ctx.respond(f"Message has not been sent. It seems like this user turned off dms.",ephemeral = True)
      await ctx.respond(f'The user {member} has been banned from the server. Reason: {reason}')
@ban.error
async def ban_error(ctx,error):
  if ban(error,MissingPermissions):
    await ctx.respond("You do not have required permission for the action performed")
  else:
    raise error  # Here we raise other errors to ensure they aren't ignored


@bot.slash_command(name = "unban", description = "Unbans a member")
@commands.has_permissions(ban_members = True)
async def unban(ctx, id: Option(discord.Member, description = "The User ID of the person you want to unban.", required = True)):
    await ctx.defer()
    member = id
    await ctx.guild.unban(member)
    await ctx.respond(f"I have unbanned {member.mention}.")
@unban.error
async def unbanerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You do not have required permission for the action performed")
    else: 
        await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
        raise error


@bot.slash_command(name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(ban_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True),*, days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.administrator:
        await ctx.respond("You can't timeout an admin!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    else:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You do not have required permission for the action performed")
    else:
        raise error


@bot.slash_command(name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(ban_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")
@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You do not have required permission for the action performed")
    else:
        raise error


@bot.slash_command(description="A private command...")
@commands.is_owner()  # This decorator will raise commands.NotOwner if the invoking user doesn't have the owner_id
async def secret(ctx, user:discord.Member, *, message: str):
  try:
    await user.send(message)
    await ctx.respond(f"Message has been sent!",ephemeral = True)
  except:
    await ctx.respond(f"Message has not been sent. It seems like this user turned off dms.",ephemeral = True)
@secret.error
async def on_application_command_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("Sorry, only the bot owner can use this command!")
    else:
        raise error  # Here we raise other errors to ensure they aren't ignored


@bot.slash_command(description="Let the bot message for you on a channel")
async def speak(ctx, *, message: str, channel_name: str):
  try:
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    channel_id = channel.id
    await bot.get_channel(int(channel_id)).send(f'{ctx.author.mention} said {message}')
    await ctx.respond("Message has been sent.",ephemeral = True)
  except:
    await ctx.respond(f"Message has not been sent. Please enter a valid channel name. Note that this command only works in a server.",ephemeral = True)


@bot.command(description="Add roles to a member")
@has_permissions(manage_roles=True)
async def addrole(ctx, user : discord.Member, role:discord.Role):
    await user.add_roles(role)
    await ctx.respond(f" Added {role} to {user.mention}")
@addrole.error
async def role_error(ctx,error):
  if addrole(error, MissingPermissions):
    await ctx.respond("You or the bot is not authorized for this action. Make sure you add a role that has lower privileges compared to the bot's role")
  else:
    raise error


def msg_contains_word(msg, word):
    return re.search(fr'\b({word})\b', msg) is not None
@discord.command()
async def loadcog(cog):
    bot.load_extension(f"cogs.{cog}")
@discord.command()
async def unloadcog(cog):
    bot.unload_extension(f"cogs.{cog}")
bannedWords={"ret"}
@bot.event
async def on_message(message):
    messageAuthor = message.author
    if bannedWords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedWord in bannedWords:
            if msg_contains_word(message.content.lower().replace(" ",""), bannedWord):
                await message.delete()
                await message.channel.send(f"{messageAuthor.mention} Message contains a banned word.")
        

async def get_pfp(user_id=int(DEV_ID)):
  # assuming you have a reference to your commands.Bot instance
  target_user = await bot.fetch_user(user_id)
  # also assuming the user_id is valid (not handling exceptions)
  return target_user.avatar.url, target_user.name


async def get_bot_pfp(user_id=int(BOT_ID)):
  # assuming you have a reference to your commands.Bot instance
  target_user = await bot.fetch_user(user_id)
  # also assuming the user_id is valid (not handling exceptions)
  return target_user.avatar.url


@bot.command(name = "about", description="Fernity's about page.")
async def about(ctx):
    embed = discord.Embed(
        title="Welcome!",
        description="Type /help for more info on commands.",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="About Me", value="The mascot of the bot is called Fern and they are a red panda. More features will be added soon in the future so be on the lookout for them :D [Click here!](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
    embed.set_footer(text="Fernity - Created on Aug 19, 2022") # footers can have icons too
    DEV_PFP,DEV_NAME = await get_pfp()
    embed.set_author(name=DEV_NAME, icon_url=DEV_PFP)
    embed.set_thumbnail(url=await get_bot_pfp())
    embed.set_image(url="https://example.com/link-to-my-banner.png")
 
    await ctx.respond("Hello! Here's my about me", embed=embed) # Send the embed with some text


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown!")
    else:
        raise error  # Here we raise other errors to ensure they aren't ignored

def get_bracket_ranges(expression):
    bracket_stack = []

    ranges = []

    for i in range(len(expression)):
        token = expression[i]

        if token == "(":
            bracket_stack.append({
                "start": i
            })
        elif token == ")":
            if not bracket_stack:
                return False

            top = bracket_stack.pop()
            top["end"] = i

            ranges.append(top)

    if bracket_stack:
        return []

    return ranges

def has_safe_powers(expression: str, suspected_expression: bool = False):
    MAX_BASE = 10
    MAX_EXPONENT = 10
    expression = expression.replace(" ", "").strip()
    ranges = get_bracket_ranges(expression)

    for i in range(1, len(expression)-1):
        if expression[i] == "^":
            if expression[i-1] == ")":
                if check_sub_expression(expression,ranges,i) is False: return False           
            else:
                num_start = i - 1
                target = ""
                while num_start >= 0 and expression[num_start].isnumeric():
                    target += expression[num_start]
                    num_start -= 1   
                
                target = "".join(reversed(target))
                print(target)
                if int(target) > MAX_BASE:
                    return False
                    
                
            if expression[i+1] == "(":
                if check_sub_expression(expression,ranges,i) is False: return False
            else:
                num_start = i + 1
                target = ""

                while num_start < len(expression) and expression[num_start].isnumeric():
                    target += expression[num_start]
                    num_start += 1   
                
                print(target)
                if int(target) > MAX_EXPONENT:
                    return False

    if suspected_expression:

        res = eval(expression.replace("^", "**"))
        if res > MAX_EXPONENT or res > MAX_BASE:
            print(res)
            return False

    return True

def check_sub_expression(expression: str, ranges: list, exp_index):
    for b_range in ranges:
        start, end = b_range["start"], b_range["end"]

        if end == exp_index - 1:
            if has_safe_powers(expression[start: end + 1], suspected_expression=True) is False:
                return False

        if start == exp_index + 1:
            if has_safe_powers(expression[start: end + 1], suspected_expression=True) is False:
                return False   

def is_safe_expression(expression : str):
    for token in expression:
        if token.isalpha():
              return False
    return True

@bot.slash_command(name="evaluate") 
async def evaluate_expression(ctx,expression : str):
  '''
  Calculates an arithmetic operation
  '''
  is_safe_expression(expression)
  expression = expression.replace("^","**")
  try:
    if is_safe_expression(expression) is False:
      await ctx.respond(f"Invalid expression syntax. Please enter a number and a math operation to calculate the result")
    elif len(expression) > 50:
      await ctx.respond("Sorry, the arithmetic operation is too long. Please shorten the expression") 
    elif has_safe_powers(expression):
      await ctx.respond("Sorry, the exponents and bases are too high. Please shorten the expression") 
    elif check_sub_expression(expression):
      await ctx.respond("Sorry, the arithmetic operation is too big. Please shorten the expression") 
    else:
      results = eval(expression)
      await ctx.respond(f"The result of that calculation is {results}")
  except ZeroDivisionError:
    await ctx.respond("Sorry, you cannot divide by zero") 
  except NameError:
    await ctx.respond(f"Invalid expression syntax. Please enter a number and a math operation to calculate the result")
  except SyntaxError:
    await ctx.respond(f"Invalid expression syntax. Please enter a number and a math operation to calculate the result")
  except:
    await ctx.respond("Sorry, the arithmetic operation is too long. Please shorten the expression")


@bot.command(name="root", description="Gets the nth root of a number")
async def root(ctx, number: int, nthroot: int):
  if number >= 0 and nthroot == 2:
    from math import sqrt 
    await ctx.respond(f"The square root of {number} is {sqrt(number)}")
  elif number < 0 and nthroot == 2:
    from cmath import sqrt
    await ctx.respond(f"The square root of {number} is {sqrt(number)}")
  elif nthroot <= 1:
    await ctx.respond(f"Sorry you cannot have a root of that")
  elif number >= 0 and nthroot > 2:
    sum = number**(1/nthroot)
    await ctx.respond(f"The {nthroot}th root of {number} is {sum}") 
  else:
    number = abs(number)
    sum = number**(1/nthroot)*-1
    await ctx.respond(f"The {nthroot}th root of {number} is {sum}j") 


bot.load_extension('cogs.interaction')
bot.load_extension('cogs.mod')
bot.load_extension('cogs.probability')
bot.load_extension('cogs.fun')
bot.run(os.getenv('DISCORD_TOKEN')) # run the bot with the token


