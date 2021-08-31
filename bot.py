# bot.py
import datetime
import os
import sqlite3
from typing import Union
import locale

from discord import Guild

import Library

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('discordToken')

bot = commands.Bot(command_prefix=('Corona', '!'))
lastEmbed = None

# locale.setlocale(locale.LC_TIME, 'pl_PL')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print()

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


class QuizCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = sqlite3.connect('quiz.db')
        self.quiz_channel = None

    @commands.command(name='options')
    async def add_option(self, ctx, emoji: Union[discord.PartialEmoji, str], *, value):
        cur = self.database.cursor()
        now = datetime.datetime.now() + datetime.timedelta(days=30)
        query = now.strftime('%B %Y').title()
        acting_quiz: tuple[str, str] = cur.execute(f"SELECT * FROM quiz WHERE [month] = '{query}'").fetchone()
        if self.quiz_channel is None:
            self.quiz_channel = self.bot.get_channel(780881100750585866)
        if acting_quiz is None:
            await self.new_quiz(ctx, emoji, value, self.quiz_channel)
        else:
            message: discord.Message = await self.quiz_channel.fetch_message(int(acting_quiz[1]))
            quiz: discord.Embed = message.embeds[0]
            quiz.description = quiz.description + f"\n{str(emoji)} {value}"
            await message.edit(embed=quiz)
            await message.add_reaction(emoji)
            await message.channel.send(".", delete_after=0.1)
        await ctx.message.add_reaction("👍")

    async def new_quiz(self, ctx, emoji: discord.PartialEmoji, value, channel: discord.TextChannel):
        now = datetime.datetime.now() + datetime.timedelta(days=30)
        quiz = discord.Embed(title=now.strftime('%B %Y').title(), colour=discord.Colour.blurple(), description=f"{str(emoji)} {value}")
        quiz.set_author(name='Głosowanie na tematykę nicków')
        cur = self.database.cursor()
        quiz_message = await channel.send("@everyone rozpoczynamy nowe głosowanie", embed=quiz)
        await quiz_message.add_reaction(emoji)
        cur.execute(f"INSERT INTO quiz VALUES ('{now.strftime('%B %Y').title()}', '{quiz_message.id}')")
        cur.close()
        self.database.commit()

    async def close_quiz(self):
        now = datetime.datetime.now()
        cur = self.database.cursor()
        query = now.strftime('%B %Y').title()
        acting_quiz: tuple[str, str] = cur.execute(f"SELECT * FROM quiz WHERE [month] = '{query}'").fetchone()
        if acting_quiz is None:
            return
        quiz_message: discord.Message = await self.quiz_channel.fetch_message(int(acting_quiz[1]))
        quiz: discord.Embed = quiz_message.embeds[0]
        quiz.description = f"***<a:GifTada:794379610246610954>Ankieta zakończona!<a:GifTada:794379610246610954>***\n" + quiz.description
        await quiz_message.edit(embed=quiz)
        cur.execute(f"DELETE FROM quiz WHERE [month] = '{query}'")
        cur.close()
        self.database.commit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.__contains__('zostaną zmienione'):
            await self.close_quiz()
            await message.add_reaction("🥳")



bot.add_cog(QuizCog(bot))
bot.run(TOKEN)

