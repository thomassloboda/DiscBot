import os

from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

import sqlite3

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DB_PATH = os.getenv('DB_PATH')
JOIN_ROLE = os.getenv('JOIN_ROLE')
COMPETITOR_ROLE = os.getenv('COMPETITOR_ROLE')
connection = sqlite3.connect(DB_PATH)
dbInstance = connection.cursor()

bot = commands.Bot(command_prefix='!')

dbInstance.execute("CREATE TABLE IF NOT EXISTS hashes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id STRING, channel_id STRING, user_name STRING, hash STRING)")
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

    shouldCreateJoin = True
    shouldCreateCompetitor = True
    for role in guild.roles:
        if role.name == JOIN_ROLE:
            shouldCreateJoin = False
        elif role.name == COMPETITOR_ROLE:
            shouldCreateCompetitor = False
    if shouldCreateJoin == True:
        print("Create role " + JOIN_ROLE)
        await guild.create_role(name=JOIN_ROLE)
    if shouldCreateCompetitor == True:
        print("Create role " + COMPETITOR_ROLE)
        await guild.create_role(name=COMPETITOR_ROLE)


async def join(ctx):
    for r in ctx.guild.roles:
        if r.name == JOIN_ROLE:
            role = r
            break
    author = ctx.message.author
    if role:
        await author.add_roles(role)
        await ctx.send(author.mention + ", you've joined the competitors")
    else:
        await ctx.send(author.mention + ", tornament now working at the moment")


async def register(ctx, hashcode):
    for r in ctx.guild.roles:
        if r.name == COMPETITOR_ROLE:
            cRole = r
        elif r.name == JOIN_ROLE:
            jRole = r
    author = ctx.message.author
    if cRole and jRole:
        dbInstance.execute("INSERT INTO hashes(user_id,channel_id,user_name,hash) VALUES (?,?,?,?)", (author.id, ctx.channel.id, author.display_name, hashcode))
        connection.commit()
        await author.remove_roles(jRole)
        await author.add_roles(cRole)
        await ctx.send(author.mention + ", you are registered with hash " + hashcode)
    else:
        await ctx.send(author.mention + ", tornament now working at the moment")

async def help(ctx):
    await ctx.message.author.send("""here is the help
    
- **!tornament join**: allow you to join the current tornament's competitors list
    
- **!tornament register {xxxx}**: allow you to register the current tornament passing your deck hash
    
    Have fun, see you soon""")

@bot.command(name="tornament", pass_context=True)
async def tornament(ctx, action, *args):
    if action == "join":
        await join(ctx)
    elif action == "register":
        await register(ctx, args[0])
    elif action == "help":
        await help(ctx)
    else:
        await ctx.send(author.mention + ", unknown commands " + args)


bot.run(TOKEN)