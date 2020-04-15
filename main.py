import os

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@bot.command(name="tornament",pass_context=True)
async def tornament(ctx, action, *args):
    author = ctx.message.author
    if action == "join":
        await ctx.send("hello " + author.display_name + ", you've joined with hash " + args[0])
    else:
        await ctx.send("hello " + author.display_name + ", unknown commands " + args)


bot.run(TOKEN)