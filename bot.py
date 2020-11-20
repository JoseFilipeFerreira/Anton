import discord
from discord.ext import commands
import asyncio 

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix = '>',
    case_insensitive=True,
    intents=intents)

def main():
    bot.STATS_PATH = "stats.json"
    bot.run(open('auth').readline().rstrip())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='>help'))

    #default color for embeds
    bot.embed_color = get_bot_color(bot)

    bot.load_extension("hungergames")

    print('Logged in as:', bot.user.name)
    print('-----------------------------')
    print('Servers:')
    for guild in bot.guilds:
        print(guild.name)
    print('-----------------------------')
    print("Color:", bot.embed_color)
    print("Prefix:", bot.command_prefix)



@bot.event
async def on_message(message):
    #send media
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)

def get_bot_color(bot):
    bGuild, color = 0, 0xffff00
    for guild in bot.guilds:
        if len(guild.members) > bGuild:
            bGuild, color = len(guild.members), guild.me.color
    return color

main()
