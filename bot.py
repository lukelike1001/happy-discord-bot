from discord.ext import commands
import discord
from datatypes import Session
import datetime

# a bot token is like a password
BOT_TOKEN = ""
CHANNEL_ID = 1202085180987146281
MAX_SESSION_TIME_MINUTES = 10

# create the bot (commands start with !)
bot = commands.Bot(command_prefix="!",
                   intents=discord.Intents.all())

# create a session for a user
session = Session()

# the bot will react to an event in the server
@bot.event
async def on_ready():
    print("Hello! Cakebot is ready. :D")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Cakebot is ready. :D")

# the bot will react to [prefix][function name] in the given context (ctx)
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

# the bot can only take string inputs
@bot.command()
async def add(ctx, *arr):
    summ = sum([int(x) for x in arr])
    await ctx.send(f"Result: {summ}")
    
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_time = ctx.message.created_at.strftime("%m/%d/%Y %H:%M:%S")
    await ctx.send(f"Session started at {human_time}")
    
    
@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_time = str(datetime.timedelta(seconds=duration))
    await ctx.send(f"Session ended after {human_time}")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Take a break! You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")

# runs the code
bot.run(BOT_TOKEN)