import os

from discord.ext import commands
from dotenv import load_dotenv

import sqlite3

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DB_PATH = os.getenv('DB_PATH')
connection = sqlite3.connect(DB_PATH)
dbInstance = connection.cursor()

bot = commands.Bot(command_prefix='!')

dbInstance.execute("CREATE TABLE IF NOT EXISTS hashes (user STRING PRIMARY KEY, hash STRING)")
connection.commit()

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
        dbInstance.execute("INSERT INTO hashes(user,hash) VALUES (?,?)", (author.display_name, args[0]))
        connection.commit()
        await ctx.send("hello " + author.display_name + ", you've joined with hash " + args[0])
    else:
        await ctx.send("hello " + author.display_name + ", unknown commands " + args)


bot.run(TOKEN)