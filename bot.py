# bot.py
import os

from discord import Guild

import Library

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('discordToken')

bot = commands.Bot(command_prefix='Corona')
lastEmbed = None


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print()


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='Bot', help="Pokazuje dane o Koronawirusie dla danego państwa")
async def cv_local(ctx, country ):
    if str(country).lower() == "world" or str(country).lower() == "kw" or str(country).lower() == "za":
        url = 'https://www.worldometers.info/coronavirus/'
        code = Library.HttpsRead(url, "świata")
        lastEmbed = code
    else:
        temp1 = Library.exceptionCheck(country)[0]
        url = 'https://www.worldometers.info/coronavirus/country/' + temp1
        code = Library.HttpsRead(url, country)
        lastEmbed = code

    await ctx.send(embed=code)
    print("User " + str(ctx.message.author.name) +"(Id: " + str(ctx.message.author.id) + ")"  + " searched for: " +
          str(Library.exceptionCheck(country)[1]))


@bot.command(name='kw', help="Pokazuje dane o Koronawirusie dla świata")
async def cv_local(ctx):
    url = 'https://www.worldometers.info/coronavirus/'
    code = Library.HttpsRead(url, "świata")
    await ctx.send(embed=code)


@bot.command(name='terminate', help="Wyłącza bota")
async def terminate(ctx):
    await ctx.send("Bye")
    await bot.close()


# @bot.command(name='Report', help="Zgłasza ostatnią wiadomość bota jako błędną")
# async def report(ctx):
#     Guild = bot.get_guild(621725816329469953)
#     member = Guild.get_member(9110)
#     await member.create_dm()
#     await member.dm_channel.send(lastEmbed)
#     await ctx.send("Zgłosiłam ostatnie dane")

bot.run(TOKEN)
