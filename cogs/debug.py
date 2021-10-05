import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time
import os.path
import sqlite3
import asyncio
import json
import requests
from Cybernator import Paginator
import jishaku
import wikipedia

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
muted = db["muted"]
black_list = db["banlist"]

class debug(commands.Cog):
    """DEBUG Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Debuger by dollar ム baby#3603 - Запущен')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return # await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Команда не найдена!', colour = 0xFB9E14))
            elif isinstance(error, commands.MissingPermissions):
                return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, У бота недостаточно прав!\n'
                f'❗ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций.', colour = 0xFB9E14), delete_after = 7)
            elif isinstance(error, commands.MissingPermissions) or isinstance(error, discord.Forbidden):
                return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, У вас недостаточно прав!', colour = 0xFB9E14), delete_after = 3)
            elif isinstance(error, commands.BadArgument):
                if "Member" in str(error):
                    if ctx.author.id == 646573856785694721:
                        ctx.command.reset_cooldown(ctx)
                    if ctx.message.content.split(' ')[0] == '!ban':
                        cmd = ctx.message.content.split(' ')
                        try:
                            memberid = int(cmd[1].replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
                            if not memberid in [i.id for i in ctx.guild.members]:
                                embed = discord.Embed(title = '\⛩️ **__Пользователь не найден__**', description = f'{ctx.author}, пользователь которого вы указали не найден на сервере `{ctx.guild.name}`.\nВы можете внести пользователя с `ID: {memberid}` в бан-лист гильдии.\n\n✅ - **Подтвердить занесение**\n❌ - **Не заносить**')
                                embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                                message = await ctx.send(f'{ctx.author.mention}', embed = embed)
                                await message.add_reaction('✅')
                                await message.add_reaction('❌')
                                try:
                                  react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
                                except Exception:
                                  ctx.command.reset_cooldown(ctx)
                                  return await message.delete()
                                else:
                                  await message.delete()
                                  if str(react.emoji) == '✅':
                                      print('+')
                                      if black_list.count_documents({"guild": ctx.guild.id, "userID": memberid}) > 0: return await ctx.send(embed = discord.Embed(title = '\⛩️ **__Ошибка занесения данных__**', description = f'❌ Пользователь с `ID: {memberid}` уже находится в бан-листе сервера `{ctx.guild.name}`'), delete_after = 10)                   
                                      try: reason = cmd[2] if not cmd[2] == None else 'Не указана'
                                      except: reason = 'Не указана'
                                      black_list.insert_one({"guild": ctx.guild.id, "userID": memberid, "moder": f'{ctx.author.name}#{ctx.author.discriminator}', "reason": reason})
                                      await ctx.send(embed = discord.Embed(title = '\⛩️ **__Успешно__**', description = f'✅ Пользователь с `ID: {memberid}` успешно занесён в бан-лист сервера `{ctx.guild.name}`\n**Причина:** `{reason}`'), delete_after = 10)
                                      embed = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at) 
                                      embed.set_author(name = f'Пользователь был занесён в бан-лист!')
                                      embed.add_field(name = 'Пользователь', value = f'**ID:** `{memberid}`', inline = False) 
                                      embed.add_field(name = 'Модератор', value = f'**{ctx.author.display_name}**`({ctx.author})`', inline = False)    
                                      embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
                                      embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                                      embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                                      channel = self.bot.get_channel(834039427541631016)
                                      logsuser = self.bot.get_channel(850605849343819836)
                                      await channel.send(embed = embed) 
                                      return await logsuser.send(embed = embed)
                                  else: return
                        except: pass      
                    return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Пользователь не найден!', colour = 0xFB9E14), delete_after = 3)
                if "Guild" in str(error):
                    if ctx.author.id == 646573856785694721:
                        ctx.command.reset_cooldown(ctx)
                    return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Сервер не найден!', colour = 0xFB9E14), delete_after = 3)
                else:
                    if ctx.author.id == 646573856785694721:
                        ctx.command.reset_cooldown(ctx)
                    return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Введён неверный аргумент!', colour = 0xFB9E14), delete_after = 3)
            elif isinstance(error, commands.MissingRequiredArgument):
                if ctx.author.id == 646573856785694721:
                    ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Пропущен аргумент с названием {error.param.name}!', colour = 0xFB9E14), delete_after = 3)
            elif isinstance(error, commands.CommandOnCooldown):
                if ctx.author.id == 646573856785694721:
                    ctx.command.reset_cooldown(ctx)
                await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Воу, Воу, Не надо так быстро использовать эту функцию.\n'
                f'❗ Подожди {error.retry_after:.2f} секунд и сможешь сделать это действие повторно'), delete_after = 5)
            else:
                # await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Произошла неизвестная ошибка. Напишите разработчику в личные сообщения для её устранения:\n> `Discord:` **dollar ム baby#3603**\n> [[В]Контайте](https://vk.com/norimyxxxo1702)'), delete_after = 5)
                raise error

def setup(bot):
    bot.add_cog(debug(bot))
