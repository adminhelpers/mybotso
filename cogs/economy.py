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
import jishaku
import wikipedia
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
dbs = cluster["RodinaBD"]
users = db["users"]
reports = dbs["reports"]
mons = db["usermon"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _iFamily) d) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

global tens
tens = [ ]

def get_user_in_guild(guild: discord.Guild, user_id):
	if int(user_id) in [i.id for i in guild.members]: return 1
	else: return 0

def get_name(guild):
	if not guild == 477547500232769536 and not guild == 577511138032484360: return
	if guild == 477547500232769536:
		return '❄️Снежинок'
	else:
		return 'Рисинок'
	
def get_guilds(guild):
	if not guild == 477547500232769536 and not guild == 577511138032484360: return
	if guild == 477547500232769536:
		return 'Северный Округ'
	else:
		return 'Восточный Округ'
	
def emb(title, text):
	embed = discord.Embed(title = f'\⛩️ **__{title}__**', description = text)
	embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
	return embed

def addbt(guild, member: discord.Member, arg : int):
	if users.count_documents({"guild": member.guild.id, "ids": member.id}) == 0:
		users.insert_one({"guild": member.guild.id, "ids": member.id, "messages": 0, "coins": arg})
		return arg
	else:
		try: 
			bal = arg + users.find_one({"guild": member.guild.id, "ids": member.id})["coins"]
			users.update_one({"guild": member.guild.id, "ids": member.id}, {"$set": {"coins": bal}})
			return bal
		except: 
			a = users.find_one({"guild": member.guild.id, "ids": member.id})
			messages = a["messages"]
			users.delete_one({"_id": a["_id"]})
			users.insert_one({"guild": member.guild.id, "ids": member.id, "messages": messages, "coins": arg})
			return arg

def rebt(guild, member: discord.Member, arg : int):
	bal = users.find_one({"guild": guild, "ids": member.id})["coins"] - arg
	users.update_one({"guild": guild, "ids": member.id}, {"$set": {"coins": bal}})
	return bal

def get_promo(guild, promocode):
	if users.count_documents({"guild_id": guild, "promocode": promocode}) == 0: return 0
	return 1

def user_promo(guild, member: discord.Member, promocode):
	promo = users.find_one({"guild_id": guild, "promocode": promocode})
	user = promo["users"]
	if member.id in user: return 1
	return 0

def use_promo(guild, member: discord.Member, promocode):
	promo = users.find_one({"guild_id": guild, "promocode": promocode})
	user = promo["users"]
	user.append(member.id)
	if promo["lent"] == 1: 
		users.delete_one({"_id": promo["_id"]})
		return promo["amount"]
	users.update_one({"_id": promo["_id"]}, {"$set": {"lent": promo["lent"] - 1, "users": user}})
	return promo["amount"]

def proverka(guild, member, stv : int):
	if users.count_documents({"guild": guild, "ids": member.id}) == 0:
		a = users.find_one({"guild": member.guild.id, "ids": member.id})
		messages = a["messages"]
		users.delete_one({"_id": a["_id"]})
		users.insert_one({"guild": member.guild.id, "ids": member.id, "messages": messages, "coins": arg})
		return 0

	else:
		if users.find_one({"guild": guild, "ids": member.id})["coins"] < stv:
			return 0
		else:
			return 1

def proc(args):
  s = 0
  if args >= 10 and args <= 30:
    s = 1
  elif args > 30 and args <= 50: 
    s = 2
  elif args > 50 and args <= 70: 
    s = 3
  elif args > 70 and args <= 90: 
    s = 4
  elif args > 90 and args <= 150: 
    s = 5
  elif args > 150: 
    s = 10

  return s


class econom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
	
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def createpromo(self, ctx, amount = None, setad: int = None, lent: int = None):
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not ctx.guild.id == 577511138032484360: return 

        if amount == None or lent == None or setad == None: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка использования команды', text = f'❌ {ctx.author}, используйте команду правильно\n\n`Пример:` **__{prefix}createpromo [name] [coin] [lent]__**\n> `name` - Название промокода\n> `coin` - Вознаграждение\n> `lent` - Количество его использований'), delete_after = 7)
        if get_promo(ctx.guild.id, amount.lower()) == 1: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка создания промокода', text = f'❌ {ctx.author}, такой промокд уже существует.\n`Введите другое название или добавьте что-нибудь в данное, например:` **__{amount.lower()}123__**'), delete_after = 7)
        embed = discord.Embed(title = '\⛩️ **__Подтвердите ваши действия__**', description = f'{ctx.author}, Вы действительно создать промокод со следующими параметрами:\n> `Название:` **__{amount}__**\n> `Вознаграждение за использование:` **__{setad} рисинок__**\n> `Количество использований:` **__{lent} раз__**\n\n✅ - **Подтвердить**\n❌ - **Отменитить действие**')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        message = await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 30)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
        except Exception:
            return await message.delete()
        else:
            await message.delete()
            if str(react.emoji) == '✅':
                users.insert_one({"guild_id": ctx.guild.id, "promocode": amount.lower(), "amount": int(setad), "lent": int(lent), "users": []})
                return await ctx.send(ctx.author.mention, embed = emb(title = 'Успешно', text = f'✅ {ctx.author}, Вы упешно создали новый промокод.\n\n**Его параметры:**\n> `Название:` **__{amount}__**\n> `Вознаграждение за использование:` **__{setad} рисинок__**\n> `Количество использований:` **__{lent} раз__**\n\nКоманды промокодов мжно найти используя {prefix}phelp'))
            else: return
		
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None: return
        if not guild.id == 477547500232769536: return

        user = self.bot.get_user(payload.user_id)
        if user.bot: pass
        else:
            emoji, channel = str(payload.emoji), self.bot.get_channel(payload.channel_id)
            if not channel.id == 915006300734251048: return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 915006300734251048: return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            if emoji == '❄️': return await memb.add_roles(discord.utils.get(guild.roles, id = 915006300734251048))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None: return
        if not guild.id == 477547500232769536: return

        user = self.bot.get_user(payload.user_id)
        if user.bot: pass
        else:
            emoji, channel = str(payload.emoji), self.bot.get_channel(payload.channel_id)
            if not channel.id == 915006300734251048: return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 915006300734251048: return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)   
            if emoji == '❄️': return await memb.remove_roles(discord.utils.get(guild.roles, id = 915006300734251048))
		
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def deletepromo(self, ctx, amount = None):
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not ctx.guild.id == 577511138032484360: return 

        if amount == None: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка использования команды', text = f'❌ {ctx.author}, используйте команду правильно\n\n`Пример:` **__{prefix}deletepromo [name]__**\n> `name` - Название промокода'), delete_after = 7)
        if get_promo(ctx.guild.id, amount.lower()) == 0: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка создания промокода', text = f'❌ {ctx.author}, такого промокода не существует'), delete_after = 7)
        embed = discord.Embed(title = '\⛩️ **__Подтвердите ваши действия__**', description = f'{ctx.author}, Вы действительно хотите удалить промокод **__{amount}__**\n\n✅ - **Подтвердить**\n❌ - **Отменитить действие**')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        message = await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 30)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
        except Exception:
            return await message.delete()
        else:
            await message.delete()
            if str(react.emoji) == '✅':
                users.delete_one({"guild_id": ctx.guild.id, "promocode": amount.lower()})
                return await ctx.send(ctx.author.mention, embed = emb(title = 'Успешно', text = f'✅ {ctx.author}, Вы упешно удалили промокод **__{amount}__**'))
            else: return
		
    @commands.command()
    async def phelp(self, ctx):
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not ctx.guild.id == 577511138032484360: return 
	
        return await ctx.send(ctx.author.mention, embed = emb(title = 'Список команд промокодов', text = f'**__{prefix}createpromo [name] [coin] [lent]__** `- Создать промокод`\n> `[name]` - Название промокода\n> `[coin]` - Вознаграждение\n> `[lent]` - Количество его использований\n\n**__{prefix}promo [name]__** `- Использовать промокод`\n> `[name]` - Название промокода\n\n**__{prefix}deletepromo [name]__** `- Удалить промокод`\n> `[name]` - Название промокода'), delete_after = 15)

		
    @commands.command()
    async def promo(self, ctx, amount = None):
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not ctx.guild.id == 577511138032484360: return 

        if amount == None: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка использования команды', text = f'❌ {ctx.author}, используйте команду правильно\n\n`Пример:` **__{prefix}promo [name]__**\n> `name` - Название промокода'), delete_after = 7)
        if get_promo(ctx.guild.id, amount.lower()) == 0: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка использования промокода промокода', text = f'❌ {ctx.author}, такого промокда не существует.\n`Проверьте правильность написания промокода, его валидность или используйте другой.`'), delete_after = 7)
        if user_promo(ctx.guild.id, ctx.author, amount.lower()) == 1: return await ctx.send(ctx.author.mention, embed = emb(title = 'Ошибка использования промокода промокода', text = f'❌ {ctx.author}, Вы уже использовали данный промокод'), delete_after = 5)
        head = use_promo(ctx.guild.id, ctx.author, amount.lower())
        addbt(ctx.guild.id, ctx.author, head)
        return await ctx.send(ctx.author.mention, embed = emb(title = 'Успешно', text = f'✅ {ctx.author}, Вы упешно активировали промокод **__{amount}__**.\n`На Ваш баланс зачислено:` **{head}** рисинок.'), delete_after = 10)
		
    @commands.command()
    async def topcoins(self, ctx):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return 
      zb = 0

      m = [ ]
      m2 = [ ]
      m3 = [ ]
      c = [ ]
      c2 = [ ]
      cz = [ ]
      cz2 = [ ]
      fr = 0
      zb = 50
      for i in users.find({"guild": ctx.guild.id}):
        try:
            mname = discord.utils.get(ctx.guild.members, id = i["ids"])
            if mname.bot: continue 
            m.append(i["coins"])
            cz.append(mname.name)

            coins = i["coins"]

            gs = get_name(ctx.guild.id)
            c.append(f'**{gs}** `{coins}`')
            fr += 1
        except: pass
      
      m2 = m
      m3 = m
      c2 = c
      cz2 = cz
      t = sorted(m)[::-1]

      frf = 0
      frfz = 0
      stra = 1
      zbs = zb//10
      if zbs == 0:
        zbs = 1
      embed = discord.Embed(title = f'Таблица лидеров', description = None, colour = 0x09F2C8)
      for v in t:
        frfz += 1
        frf += 1
        f = m2.index(v)
        if frf == 1:
          frs = f'🥇 1. {cz[f]}'
        elif frf == 2:
          frs = f'🥈 2. {cz[f]}'
        elif frf == 3:
          frs = f'🥉 3. {cz[f]}'
        else:
          frs = f'{frf}. {cz[f]}'
        embed.add_field(name = frs, value = c[f], inline = False)
        c.remove(c[f])
        cz.remove(cz[f])
        m2.remove(m2[f])
        if frfz == 10:
          frfz = 0
          break     

      mes = await ctx.send(embed = embed)

    @commands.command()
    async def mtest(self, ctx):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360:
        return
      m = [ ]
      for i in users.find():
        if i["messages"] > 20000: 
          try: m.append(f'{discord.utils.get(ctx.guild.members, id = i["ids"]).name} - {i["messages"]} coins')
          except: m.append(f'Неизвестный тип с ID: {i["ids"]} - {i["messages"]} coins')
      print(m)

    @commands.command(aliases = ["hwen"])
    async def hallowen(self, ctx):
      if not ctx.guild.id == 477547500232769536: return
      embed = discord.Embed(title = 'Мороз и солнце, день чудесный!', description = f'\❄️ **Кажется, согласно календарю, у всех уже наступила зима!** \❄️\n\nБелый снег, пушистый в воздухе кружится\nИ на землю тихо падает, ложится.\n\n**В предверии праздников, хотим порадовать тебя очередной халявной ролью!\👀 Нажми на зимнюю реакцию \❄️ и бот сделает тебе подарок.**', color = 0x0CDEE7)
      embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
      embed.set_thumbnail(url = ctx.guild.icon_url)
      await ctx.message.delete()
      return await ctx.send('@everyone', embed = embed)
	
    @commands.command(aliases = ["mtop"])
    async def topmessages(self, ctx):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360:
        return
      zb = 0

      m = [ ]
      m2 = [ ]
      m3 = [ ]
      c = [ ]
      c2 = [ ]
      cz = [ ]
      cz2 = [ ]
      fr = 0
      zb = 50
      for i in users.find({"guild": ctx.guild.id}):
        if ctx.guild.id == 477547500232769536:
          if i["messages"] < 5000: continue 
        try:
          mname = discord.utils.get(ctx.guild.members, id = i["ids"])
          if mname.bot: continue
          m.append(i["messages"])
          cz.append(mname.name)
        
          coins = i["messages"]

          c.append(f'**Сообщений:** `{coins}`')
        except: pass

      
      t = sorted(m)[::-1]
      m2 = m
      m3 = m
      c2 = c
      cz2 = cz
      t = sorted(m)[::-1]

      frf = 0
      frfz = 0
      stra = 1
      zbs = zb//10
      if zbs == 0:
        zbs = 1
      embed = discord.Embed(title = f'Таблица лидеров', description = None, colour = 0xFB9E14)
      for v in t:
        frfz += 1
        frf += 1
        f = m2.index(v)
        if frf == 1:
          frs = f'💎 1. {cz[f]}'
        elif frf == 2:
          frs = f'🔥 2. {cz[f]}'
        elif frf == 3:
          frs = f'✨ 3. {cz[f]}'
        else:
          frs = f'{frf}. {cz[f]}'
        embed.add_field(name = frs, value = c[f], inline = False)
        c.remove(c[f])
        cz.remove(cz[f])
        m2.remove(m2[f])
        if frfz == 15:
          frfz = 0
          break     

      mes = await ctx.send(embed = embed)


		
    @commands.command()
    async def coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360:
            return

      if member == None:
        member = ctx.author

      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)
      gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
      pb = '❄️Снежинок' if ctx.guild.id == 477547500232769536 else 'Рисинок'

      if users.count_documents({"guild": ctx.guild.id, "ids": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'Никнейм: {member.mention}\n{pb}: `0`', colour = 0x09F2C8))

      else:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'Никнейм: {member.mention}\n{pb}: `{users.find_one({"guild": ctx.guild.id, "ids": member.id})["coins"]}`', colour = 0x09F2C8))

    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addcoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)
      gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
      pb = "`❄️Снежинок`" if ctx.guild.id == 477547500232769536 else 'рисинок'

      if member == None:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**Укажите пользователя**', colour = 0x09F2C8), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{member.mention}, укажите кол-во добавляемых {pb}**', colour = 0x09F2C8), delete_after = 5)

      if users.count_documents({"guild": ctx.guild.id, "id": member.id}) == 0:
        a = addbt(ctx.guild.id, member, amount)
        await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{ctx.author.mention}, вы добавили пользователю {member.mention} `{amount}` {pb}.\nЕго баланс: `{a}` {pb}**', colour = 0x09F2C8))
      else:
        a = addbt(ctx.guild.id, member, amount)
        channel = self.bot.get_channel(841588696334598154) if ctx.guild.id == 477547500232769536 else self.bot.get_channel(872186550715301910)
        try:
          await channel.send(embed = discord.Embed(title = 'Выдача', description = f'**Модератор {ctx.author.mention} выдал {pb} пользователю {member.mention} в размере `{amount}`**', colour = 0x25f20a, timestamp = ctx.message.created_at))
        except:
          pass
        await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{ctx.author.mention}, вы добавили пользователю {member.mention} `{amount}` {pb}.\nЕго баланс: `{a}` {pb}**', colour = 0x09F2C8), delete_after = 10)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def removecoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
	  
      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)
      gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
      pb = "`❄️Снежинок`" if ctx.guild.id == 477547500232769536 else 'рисинок'

      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{ctx.author.mention}, укажите пользователя**', colour = 0x09F2C8), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{ctx.author.mention}, укажите кол-во убираемых {pb}**', colour = 0x09F2C8), delete_after = 5)
      
      a = proverka(ctx.guild.id, member, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{ctx.author.mention}, пользователь не имеет такого кол-ва {pb}!**', colour = 0x09F2C8))
      else:
        bal = rebt(ctx.guild.id, member, amount)
        channel = self.bot.get_channel(841588696334598154) if ctx.guild.id == 477547500232769536 else self.bot.get_channel(872186550715301910)
        await channel.send(embed = discord.Embed(title = 'Снятие', description = f'**Модератор {ctx.author.mention} снял {pb} пользователю {member.mention} в размере `{amount}`**', colour = 0x25f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = f'{gguild} | {gs}', description = f'**{ctx.author.mention}, вы удалили у пользователя {member.mention} `{amount}` {pb}.\nЕго баланс: `{bal}` {pb}**', colour = 0x09F2C8), delete_after = 10)    

    @commands.command()
    async def pay(self, ctx, member: discord.Member = None, amount:int = None):
      global tens
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return

      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)
      gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
      pb = "`❄️Снежинок`" if ctx.guild.id == 477547500232769536 else 'рисинок'

      if ctx.author.id in tens: return await ctx.send(embed = emb(title = 'Ошибка использования команды', text = '❌ Вы не можете передавать деньги пока играете в казино!'))

      if member == None:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, укажите пользователя**', colour = 0x09F2C8), delete_after = 5)
      
      if member == ctx.author or member.bot:
        return

      if amount == None:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, укажите сумму {pb} которую нужно передать!**', colour = 0x09F2C8), delete_after = 5)

      if amount <= 0:
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, указан неверный аргумент!**', colour = 0x09F2C8), delete_after = 5)


      a = proverka(ctx.guild.id, ctx.author, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, Вы не можете передать такую сумму!**', colour = 0x09F2C8))

      else:
        bal = addbt(ctx.guild.id, member, amount)
        bal2 = rebt(ctx.guild.id, ctx.author, amount)
        channel = self.bot.get_channel(841588696334598154) if ctx.guild.id == 477547500232769536 else self.bot.get_channel(872186550715301910)
        await channel.send(embed = discord.Embed(title = 'Перевод', description = f'**Пользователь {ctx.author.mention}, передал {gs} пользователю {member.mention} в размере `{amount}`**', colour = 0x25f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, Вы передали пользователю {member.mention} `{amount}` {pb}.\nЕго баланс: `{bal}` {pb}\nВаш баланс: `{bal2}` {pb}**', colour = 0x09F2C8))
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def casino(self, ctx, amount : int = None):
      global tens
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return

      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)
      gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
      pb = "`❄️Снежинок`" if ctx.guild.id == 477547500232769536 else 'рисинок'
	
      if ctx.guild.id == 477547500232769536:
        if not ctx.channel.id == 818222772215349328:
            await ctx.message.delete()
            return await ctx.send(embed = discord.Embed(description = f'**Команда `!casino` доступна только в канале <#818222772215349328>**', colour = 0x09F2C8), delete_after = 5)
      else:
        if not ctx.channel.id == 756183285188788306:
            await ctx.message.delete()
            return await ctx.send(embed = discord.Embed(description = f'**Команда `!casino` доступна только в канале <#756183285188788306>**', colour = 0x09F2C8), delete_after = 5)
        
      if amount == None:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, укажите кол-во {pb} которое необходимо поставить!**', colour = 0x09F2C8))

      if amount <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, неверный аргумент!**', colour = 0x09F2C8))
 
      a = proverka(ctx.guild.id, ctx.author, amount)
      if a == 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, Вы не можете сделать такую ставку!**', colour = 0x09F2C8))
      else:
        tens.append(ctx.author.id)
        await ctx.send(embed = discord.Embed(title = f'Северный Округ | {gb}', description = f'**{ctx.author.mention}, Отдохни минутку и получишь результат!**', colour = 0x09F2C8))
        a = random.randint(1, 2)
        if a == 1:
            await asyncio.sleep(5)
            bal = rebt(ctx.guild.id, ctx.author, amount)
            await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, к сожалению, вы проиграли!\nТеперь Ваш баланс составляет: `{bal}` {pb}!**', colour = 0xff0000))
            tens.remove(ctx.author.id)
        if a == 2:
            amount *= 1
            await asyncio.sleep(5)
            f = amount
            bal = addbt(ctx.guild.id, ctx.author, f)
            tens.remove(ctx.author.id)
            return await ctx.send(embed = discord.Embed(title = f'{gguild} | {gb}', description = f'**{ctx.author.mention}, Вам повезло, вы удвоили свою ставку!!\nТеперь Ваш баланс составляет: `{bal}` {pb}!**', colour = 0x25f20a))

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def reset_coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
	  
      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)
      gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
      pb = "`❄️Снежинок`" if ctx.guild.id == 477547500232769536 else 'рисинок'

      if not member:
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя!```', delete_after = 5)

      if ctx.author.top_role.position <= member.top_role.position:
        return

      if coins.count_documents({"guild": ctx.guild.id, "id": member.id}) != 0:
        users.update_one({"guild": ctx.guild.id, "ids": member.id}, {"$set": {"coins": 0}})
      else:
        pass

      gf = "`d-coin's`" if ctx.guild.id == 477547500232769536 else 'рисинки'
      channel = self.bot.get_channel(841588696334598154) if ctx.guild.id == 477547500232769536 else self.bot.get_channel(872186550715301910)
      await channel.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил {gs} пользователю {member.mention}!**', colour = 0x25f20a, timestamp = ctx.message.created_at))
      return await ctx.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил {gs} пользователю {member.mention}!**', colour = 0x25f20a), delete_after = 10)      
  
    @commands.command(aliases = ['mmenu', 'сменю'])
    async def message_menu(self, ctx, member: discord.Member = None):
        dt = datetime.datetime.now()
        if ctx.guild == None: return
        if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
        await ctx.message.delete()
        mas = [743887697327816705, # Заместитель Гл. Модератора
	       661284961428701209, # Глав. Модерация Discord
	       714504039072661545, # Supervisor Moderation
	       894702472826871850] # Машулька мурлёнок
        a = 0
        for i in ctx.author.roles:
            if i.id in mas: a = 1

        if a == 0: return await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = '\⛩️ **__Ошибка доступа__**', description = f'Вам не доступна данная команда, потому что Вы:\n> `◘ Не являетесь модератором`\n> `◘ Ваш ранг модератора слишком мал.`'), delete_after = 5)
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if member != None:
            embed = discord.Embed(title = '\⛩️ **__Управление сообщениями__**', description = f'Привет, {ctx.author}, ты попал в меню управления сообщениями пользователя {member.mention}`({member})`\n\n`Вот список доступных для вас действий:`\n\n`•` 1⃣ - Проверить количество сообщений пользователя.\n`•` 2⃣ - Обнулить недельную статистику сообщений\n`•` 3⃣ - Обнулить сообщения за сегодня.\n\n\n> ❌ - **Закрыть меню**')
            message = await ctx.send(f'{ctx.author.mention}', embed = embed)
            await message.add_reaction('1⃣')
            await message.add_reaction('2⃣')
            await message.add_reaction('3⃣')
            await message.add_reaction('4⃣')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['1⃣', '2⃣', '3⃣', '4⃣', '❌'])
            except Exception:
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌': return
                elif str(react.emoji) == '1⃣':
                    if mons.count_documents({"guild": ctx.guild.id, "ids": ctx.author.id}) == 0: mons.insert_one({"guild": ctx.guild.id, "ids": ctx.author.id, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0, "date": int(dt.strftime("%d"))})
                    m = mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})
                    mons_list, mons_info, mons_name = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], [], {"monday": "Понедельник", "tuesday": "Вторник", "wednesday": "Среда", "thursday": "Четверг", "friday": "Пятница", "saturday": "Суббота", "sunday": "Воскресенье"}
                    for i in mons_list:
                        if i != dt.strftime("%A").lower(): mons_info.append(f'`• | {mons_name[i]}` - {m[i]} сообщений\n')
                        else: 
                            mons_info.append(f'`• | {mons_name[i]}` - {m[i]} сообщений\n')
                            mon_full = int(m["monday"]) + int(m["tuesday"]) + int(m["wednesday"]) + int(m["thursday"]) + int(m["friday"]) + int(m["saturday"]) + int(m["sunday"])
                            mons_info.append(f'`• | Всего сообщений за неделю:` - {mon_full}\n')
                            user_full_messages = users.find_one({"guild": ctx.guild.id, "ids": member.id})["messages"]

                            mons_info.append(f'`• | Всего сообщений за всё время:` - {user_full_messages}\n')
                            break
                    str_a = ''.join(mons_info)
                    return await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = '\⛩️ **__Управление сообщениями__**', description = f'✅ {ctx.author}, вот статистика сообщений пользователя {member.mention}`({member})`:\n\n{str_a}'))

                elif str(react.emoji) == '2⃣':
                    if mons.count_documents({"guild": ctx.guild.id, "ids": ctx.author.id}) == 0: mons.insert_one({"guild": ctx.guild.id, "ids": ctx.author.id, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0, "date": int(dt.strftime("%d"))})
                    m = mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})
                    mons_list, mons_info, mons_name = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], [], {"monday": "Понедельник", "tuesday": "Вторник", "wednesday": "Среда", "thursday": "Четверг", "friday": "Пятница", "saturday": "Суббота", "sunday": "Воскресенье"}
                    embed = discord.Embed(title = '\⛩️ **__Подтвердите ваши действия__**', description = f'{ctx.author}, Вы действительно хотите обнулить статистику сообщений за неделю у пользователя {member.mention}`({member})`?\n\n✅ - **Подтвердить**\n❌ - **Отменитить действие**')
                    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                    message = await ctx.send(f'{ctx.author.mention}', embed = embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    try: react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
                    except Exception: return await message.delete()
                    else:
                        await message.delete()
                        if str(react.emoji) == '✅':
                            embed = discord.Embed(title = '\⛩️ **__Успешно__**', description = f'✅ {ctx.author}, Вы обнулили статистику сообщений за неделю пользователю {member.mention}`({member})`')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            await ctx.send(embed = embed)
                            mons.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {"monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0}})
                        elif str(react.emoji) == '❌':
                            embed = discord.Embed(title = f'❌ {ctx.author}, Вы отменили действие.')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            return await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 5)
                elif str(react.emoji) == '3⃣':
                    if mons.count_documents({"guild": ctx.guild.id, "ids": ctx.author.id}) == 0: mons.insert_one({"guild": ctx.guild.id, "ids": ctx.author.id, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0, "date": int(dt.strftime("%d"))})
                    m = mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})
                    mons_list, mons_info, mons_name = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], [], {"monday": "Понедельник", "tuesday": "Вторник", "wednesday": "Среда", "thursday": "Четверг", "friday":"Пятница", "saturday":"Суббота", "sunday":"Воскресенье"}
                    embed = discord.Embed(title = '\⛩️ **__Подтвердите ваши действия__**', description = f'{ctx.author}, Вы действительно хотите обнулить статистику сообщений за сегодняшний день у пользователя {member.mention}`({member})`?\n\n✅ - **Подтвердить**\n❌ - **Отменитить действие**')
                    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                    message = await ctx.send(f'{ctx.author.mention}', embed = embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    try: react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
                    except Exception: return await message.delete()
                    else: 
                        await message.delete()
                        if str(react.emoji) == '✅':
                            embed = discord.Embed(title = '\⛩️ **__Успешно__**', description = f'✅ {ctx.author}, Вы обнулили статистику сообщений за сегодняшний день пользователю {member.mention}`({member})`')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            await ctx.send(embed = embed)
                            mons.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {dt.strftime("%A").lower(): 0}})
                        elif str(react.emoji) == '❌':
                            embed = discord.Embed(title = f'❌ {ctx.author}, Вы отменили действие.')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            return await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 5)
        else:
            embed = discord.Embed(title = '\⛩️ **__Управление сообщениями__**', description = f'Привет, {ctx.author}, ты попал в меню управления сообщений на сервере `{ctx.guild.name}`\n\n`Вот список доступных для вас действий:`\n\n`•` 1⃣ - Показать общий топ сообщений за неделю\n`•` 2⃣ - Обнулить недельные сообщения\n\n> ❌ - **Закрыть меню**')
            message = await ctx.send(f'{ctx.author.mention}', embed = embed)
            await message.add_reaction('1⃣')
            await message.add_reaction('2⃣')
            await message.add_reaction('❌')
            try: react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['1⃣', '2⃣', '❌'])
            except Exception: return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌': return
                elif str(react.emoji) == '1⃣':
                    user_list, user_messages, user_request, win_content = [], [], [], []
                    for user in mons.find({"guild": ctx.guild.id}):
                        if get_user_in_guild(ctx.guild, user["ids"]) == 0: continue
                        member = discord.utils.get(ctx.guild.members, id = user["ids"])
                        if member.bot: continue
                        messages = int(user["monday"]) + int(user["tuesday"]) + int(user["wednesday"]) + int(user["thursday"]) + int(user["friday"]) + int(user["saturday"]) + int(user["sunday"])
                        if messages < 1: continue
                        user_messages.append(messages)
                        user_list.append(member.display_name)
                        user_request.append(f'`Сообщений за неделю:` **{messages}**')
                    user_list_copy, sort_messages, index_win = user_messages, sorted(user_messages)[::-1], 0
                    for index_massive in sort_messages:
                        index_win += 1
                        index_coins = user_list_copy.index(index_massive)
                        user_list_copy.pop(index_coins)
                        if index_win == 1:
                            message = f'🥇 **{user_list[index_coins]}**\n    `•` {user_request[index_coins]}\n\n'
                        elif index_win == 2:
                            message = f'🥈 **{user_list[index_coins]}**\n    `•` {user_request[index_coins]}\n\n'
                        elif index_win == 3:
                            message = f'🥉 **{user_list[index_coins]}**\n    `•` {user_request[index_coins]}\n\n'
                        else:
                            message = f'`{index_win}.` **{user_list[index_coins]}**\n    `•` {user_request[index_coins]}\n\n'
                        win_content.append(message)
                        user_list.pop(index_coins)
                        user_request.pop(index_coins)
                        if index_win == 10: break
                    answer = ''.join(win_content)
                    embed = discord.Embed(title = '\⛩️ **__Топ участников по сообщениям за неделю__**', description = answer)
                    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                    message = await ctx.send(f'{ctx.author.mention}', embed = embed)
                elif str(react.emoji) == '2⃣':
                    embed = discord.Embed(title = '\⛩️ **__Подтвердите ваши действия__**', description = f'{ctx.author}, Вы действительно хотите обнулить недельную статистику сообщений всем пользователям?\n\n✅ - **Подтвердить**\n❌ - **Отменитить действие**')
                    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                    message = await ctx.send(f'{ctx.author.mention}', embed = embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')
                    try: react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
                    except Exception: return await message.delete()
                    else: 
                        await message.delete()
                        if str(react.emoji) == '✅':
                            embed = discord.Embed(title = '\⛩️ **__Успешно__**', description = f'✅ {ctx.author}, Вы обнулили недельную статистику сообщений всем пользователям.')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            await ctx.send(embed = embed)
                            for i in mons.find({"guild": ctx.guild.id}):
                                mons.update_one({"_id": i["_id"]}, {"$set": {"monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0, "date": int(dt.strftime("%d"))}})
                        elif str(react.emoji) == '❌':
                            embed = discord.Embed(title = f'❌ {ctx.author}, Вы отменили действие.')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            return await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 5)

		    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        dt = datetime.datetime.now()
        if ctx.guild == None: return
        if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return

        gguild = get_guilds(ctx.guild.id)
        gs = get_name(ctx.guild.id)
        gb = "`❄️Снежинки`" if ctx.guild.id == 477547500232769536 else 'Рисинки'
        pb = "`❄️Снежинок`" if ctx.guild.id == 477547500232769536 else 'рисинок'

        if users.count_documents({"guild": ctx.guild.id, "ids": ctx.author.id}) == 0:
            users.insert_one({"guild": ctx.guild.id, "ids": ctx.author.id, "messages": 0})
            mons.insert_one({"guild": ctx.guild.id, "ids": ctx.author.id, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0, "date": int(dt.strftime("%d"))})
            a = users.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})["messages"]
            users.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {"messages": a + 1}})
            one, two = dt.strftime("%A"), dt.strftime("%d")
            b = mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})[one.loser()]
            if int(two) == mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})["date"]: mons.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {one.lower(): b + 1}})
            else: 
                mons.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {one.lower(): 1, "date": int(two)}})
        else:
            if mons.count_documents({"guild": ctx.guild.id, "ids": ctx.author.id}) == 0: mons.insert_one({"guild": ctx.guild.id, "ids": ctx.author.id, "monday": 0, "tuesday": 0, "wednesday": 0, "thursday": 0, "friday": 0, "saturday": 0, "sunday": 0, "date": int(dt.strftime("%d"))})
            a = users.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})["messages"]
            users.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {"messages": a + 1}})
            one, two = dt.strftime("%A"), dt.strftime("%d")
            b = mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})[one.lower()]
            if int(two) == mons.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})["date"]: mons.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {one.lower(): b + 1}})
            else: 
                mons.update_one({"guild": ctx.guild.id, "ids": ctx.author.id}, {"$set": {one.lower(): 1, "date": int(two)}})

        st = 0
        if len(list(ctx.content)) >= 4:
            msgs = users.find_one({"guild": ctx.guild.id, "ids": ctx.author.id})["messages"]
            if msgs in [2000, 5000, 10000, 20000, 30000]:
                if ctx.guild.id == 477547500232769536:
                    give = {2000: f"**3** `{pb}`", 5000: f"**5** `{pb}`", 10000: f"**10** `{pb}`", 20000: f"**15** `{pb}`", 30000: f"**20** `{pb} и уникальная роль` <@&855358889067675649>"}
                else:
                    give = {2000: f"**3** `{pb}`", 5000: f"**5** `{pb}`", 10000: f"**10** `{pb}`", 20000: f"**15** `{pb}`", 30000: f"**20** `{pb}`"}
                st = {2000: 3, 5000: 5, 10000: 10, 20000: 15, 30000: 20}
                embed = discord.Embed(title = f'Достижение {ctx.author.name}', description = f'🎉 `Написать` {msgs} `сообщений!`\n✨ Награда за выполнение: {give[msgs]}', colour = 0xFB9E14)
                embed.set_thumbnail(url = ctx.author.avatar_url)
                await ctx.channel.send(embed = embed)
                addbt(ctx.guild.id, ctx.author, st[msgs])
                if ctx.guild.id == 477547500232769536:
                    if st[msgs] == 20: 
                        return await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id = 855358889067675649))

    @commands.command(aliases = ["mset"])
    @commands.has_permissions(administrator = True)
    async def setmessages(self, ctx, member: discord.Member = None, count: int = None):
        if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return


        if member == None or count == None: return await ctx.message.delete()
   
        if users.count_documents({"guild": ctx.guild.id, "ids": member.id}) == 0: users.insert_one({"ids": member.id, "messages": count})
        else: users.update_one({"guild": ctx.guild.id, "ids": member.id}, {"$set": {"messages": count}})
        return await ctx.send('Выполнено!', delete_after = 3)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return
       
        if not message.guild.id == 477547500232769536:
            return

        if message.author.bot:
            return

        a = users.find_one({"guild": message.guild.id, "ids": message.author.id})["messages"]
        users.update_one({"guild": message.guild.id, "ids": message.author.id}, {"$set": {"messages": a - 1}})

    @commands.command(aliases = ["награды", "allachive"])
    async def __prizs(self, ctx):
        if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return

        gguild = get_guilds(ctx.guild.id)
        gs = get_name(ctx.guild.id)
        gb = '❄️Снежинки' if ctx.guild.id == 477547500232769536 else 'Рисинки'
        pb = '❄️Снежинок' if ctx.guild.id == 477547500232769536 else 'рисинок'
	
        if ctx.guild.id == 477547500232769536:
            embed = discord.Embed(title = 'Награды за сообщения', description = f"За активность в чате можно не только прокачивать свой уровень, но и зарабатывать Discord-Coins`({gb})` – Валюту нашего дискорд-сервера\n\n**Список наград:**\n✨ 2000 сообщений - **3** `{pb}`\n💸 5000 сообщений - **5** `{pb}`\n🔥 10000 сообщений - **10** `{pb}`\n🎀 20000 сообщений - **15** `{pb}`\n💎 30000 сообщений - **20** `{pb} и уникальная роль` <@&855358889067675649>", color = 0xFB9E14)
        else:
            embed = discord.Embed(title = 'Награды за сообщения', description = f"За активность в чате можно не только прокачивать свой уровень, но и зарабатывать Discord-Coins`({gb})` – Валюту нашего дискорд-сервера\n\n**Список наград:**\n✨ 2000 сообщений - **3** `{pb}`\n💸 5000 сообщений - **5** `{pb}`\n🔥 10000 сообщений - **10** `{pb}`\n🎀 20000 сообщений - **15** `{pb}`\n💎 30000 сообщений - **20** `{pb}`", color = 0xFB9E14)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        return await ctx.send(embed = embed)

    @commands.command(aliases = ["messages", "сообщения"])
    async def __message(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return

      gguild = get_guilds(ctx.guild.id)
      gs = get_name(ctx.guild.id)

      if member == None:
        member = ctx.author

	
      if users.count_documents({"guild": ctx.guild.id, "ids": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = f'🏆 {gguild} | Сообщений', description = f'Никнейм: {member.mention}\nСообщений: `0`', colour = 0x09F2C8))

      else:
        return await ctx.send(embed = discord.Embed(title = f'🏆 {gguild} | Сообщений', description = f'Никнейм: {member.mention}\nСообщений: `{users.find_one({"guild": ctx.guild.id, "ids": member.id})["messages"]}`', colour = 0x09F2C8))

    @commands.command()
    async def achive(self, ctx):
    	if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360:
            return
            
    	achive = []
    	msgs = users.find_one({"id": ctx.author.id})["messages"]

    	if msgs >= 2000:
    		achive.append('[✅] Написать `2000` сообщений\n')
    	else:
    		achive.append('[❌] Написать `2000` сообщений\n')
    	if msgs >= 5000:
    		achive.append('[✅] Написать `5000` сообщений\n')
    	else:
    		achive.append('[❌] Написать `5000` сообщений\n')

    	str_a = ''.join(achive)
    	embed = discord.Embed(title = f"`💰 Ачивки пользователя {ctx.author.name}`", colour = discord.Colour.blue())
    	embed.add_field(name = '♦ Сообщения:', value = f'{str_a}')
    	embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    	await ctx.send(embed = embed)
      
def setup(bot):
    bot.add_cog(econom(bot))



'''
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
from pymongo import Mongobot

cluster = Mongobot("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
report = db["report"]
coins = db["coins"]
users = db["users"]

def addbs(member, arg):
  if users.count_documents({"id": member}) == 0:
    users.insert_one({"id": member, "vsv": 0, "messages": 0})
    bal = 1 + users.find_one({"id": member})[arg]
    users.update_one({"id": member}, {"$set": {arg: bal}})
    return bal
  else:
    bal = 1 + users.find_one({"id": member})[arg]
    users.update_one({"id": member}, {"$set": {arg: bal}})
    return bal

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

global tens
tens = [ ]

def addbt(member: discord.Member, arg : int):
  if coins.count_documents({"guild": ctx.guild.id, "id": member.id}) == 0:
    coins.insert_one({"guild": member.guild.id, "id": member.id, "coins": arg})
    return arg
  else:
    bal = arg + coins.find_one({"guild": ctx.guild.id, "id": member.id})["coins"]
    coins.update_one({"guild": ctx.guild.id, "id": member.id}, {"$set": {"coins": bal}})
    return bal

def rebt(member: discord.Member, arg : int):
  bal = coins.find_one({"guild": ctx.guild.id, "id": member.id})["coins"] - arg
  coins.update_one({"guild": ctx.guild.id, "id": member.id}, {"$set": {"coins": bal}})
  return bal

def proverka(member, stv : int):
  if coins.count_documents({"guild": ctx.guild.id, "id": member.id}) == 0:
    return 0

  else:
    if coins.find_one({"guild": ctx.guild.id, "id": member.id})["coins"] < stv:
      return 0
    else:
      return 1

def proc(args):
  s = 0
  if args >= 10 and args <= 30:
    s = 1
  elif args > 30 and args <= 50: 
    s = 2
  elif args > 50 and args <= 70: 
    s = 3
  elif args > 70 and args <= 90: 
    s = 4
  elif args > 90 and args <= 150: 
    s = 5
  elif args > 150: 
    s = 10

  return s


class econom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
    
    @commands.command()
    async def topcoins(self, ctx):
      if not ctx.guild.id == 577511138032484360:
        return

      if ctx.channel.id == 756183285188788306:
        return await ctx.message.delete()

      await ctx.message.delete()

      usr = db["users"]
      coins = db["coins"]
      zb = 0

      m = [ ]
      m2 = [ ]
      m3 = [ ]
      c = [ ]
      c2 = [ ]
      cz = [ ]
      cz2 = [ ]
      fr = 0
      zb = 50
      for i in coins.find({"guild": ctx.guild.id}):
        mname = discord.utils.get(ctx.guild.members, id = i["id"])
        if mname == None:
          continue
        m.append(i["coins"])
        cz.append(mname.name)

        coins = i["coins"]

        if usr.count_documents({"id": mname.id}) == 1:
          if usr.find_one({"id": mname.id})["messages"] < 0:
            msgs = 0
          else:
            msgs = usr.find_one({"id": mname.id})["messages"]
          
          if usr.find_one({"id": mname.id})["vsv"] < 0:
            voices = f'00:00:00'
          else:
            seconds = usr.find_one({"id": mname.id})["vsv"]
            seconds = seconds % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            voices = f'{hours}:{minutes}:{seconds}'
        else:
          voices = f'00:00:00'
          msgs = 0

        c.append(f'**Коинов:** {coins} | **Сообщений:** {msgs} | 🎤 **{voices}**')
        fr += 1
        if fr >= 50:
          break
      
      m2 = m
      m3 = m
      c2 = c
      cz2 = cz
      t = sorted(m)[::-1]

      frf = 0
      frfz = 0
      stra = 1
      zbs = zb//10
      if zbs == 0:
        zbs = 1
      embed = discord.Embed(title = f'Таблица лидеров', description = f'**Страница `{stra}` из `5`**', colour = 0xFB9E14)
      for v in t:
        frfz += 1
        frf += 1
        f = m2.index(v)
        if frf == 1:
          frs = f'🥇 #1. {cz[f]}'
        elif frf == 2:
          frs = f'🥈 #2. {cz[f]}'
        elif frf == 3:
          frs = f'🥉 #3. {cz[f]}'
        else:
          frs = f'#{frf}. {cz[f]}'
        embed.add_field(name = frs, value = c[f], inline = False)
        c.remove(c[f])
        cz.remove(cz[f])
        m2.remove(m2[f])
        if frfz == 10:
          frfz = 0
          break     

      mes = await ctx.send(embed = embed)
      r_list = ['⬅', '➡', '⏺']
      for g in r_list:
        await mes.add_reaction(g)
      for i in range(100):
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 100.0, check = lambda react, user: user == ctx.author and react.emoji in r_list)
        except Exception:
          try:
            await mes.delete()
          except:
            pass
        else:
          if react.emoji == '⏺':
            try:
              await mes.delete()
            except: 
              pass
          elif react.emoji == '➡':
            if stra == zbs:
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)
            else:
              m2 = []
              for fl in m3:
                m2.append(fl)

              c = []
              for fk in c2:
                c.append(fk)

              cz = []
              for fk in cz2:
                cz.append(fk)

              stra += 1
              embed = discord.Embed(title = f'Таблица лидеров', description = f'**Страница `{stra}` из `{zbs}`**', colour = 0xFB9E14)
              frf = (stra * 10) - 10
              for v in t:
                frfz += 1
                frf += 1
                s = frf - 1
                try:
                  f = m2.index(t[s])
                except:
                  frf -= 1
                  continue
                if frf == 1:
                  frs = f'🥇 #1. {cz[f]}'
                elif frf == 2:
                  frs = f'🥈 #2. {cz[f]}'
                elif frf == 3:
                  frs = f'🥉 #3. {cz[f]}'
                else:
                  frs = f'#{frf}. {cz[f]}'
                embed.add_field(name = frs, value = c[f], inline = False)
                c.remove(c[f])
                cz.remove(cz[f])
                m2.remove(m2[f])
                if frfz == 10:
                  frfz = 0
                  break 

              try:
                await mes.edit(embed = embed)   
              except:
                pass
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)

          elif react.emoji == '⬅':
            if stra == 1:
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)
            else:
              m2 = [ ]
              for fl in m3:
                m2.append(fl)
              
              c = []
              for fk in c2:
                c.append(fk)

              cz = []
              for fk in cz2:
                cz.append(fk)
              stra -= 1
              embed = discord.Embed(title = f'Таблица лидеров', description = f'**Страница `{stra}` из `{zbs}`**', colour = 0xFB9E14)
              frf = (stra * 10) - 10
              frfz = 0
              for v in t:
                frfz += 1
                frf += 1
                s = frf - 1
                try:
                  f = m2.index(t[s])
                except:
                  frf += 1
                  continue
                if frf == 1:
                  frs = f'🥇 #1. {cz[f]}'
                elif frf == 2:
                  frs = f'🥈 #2. {cz[f]}'
                elif frf == 3:
                  frs = f'🥉 #3. {cz[f]}'
                else:
                  frs = f'#{frf}. {cz[f]}'
                embed.add_field(name = frs, value = c[f], inline = False)
                c.remove(c[f])
                cz.remove(cz[f])
                m2.remove(m2[f])
                if frfz == 10:
                  frfz = 0
                  break 
              try:
                await mes.edit(embed = embed)   
              except:
                pass 
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 325607843547840522:
            return
        if payload.member.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 757601724122005616:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 758135039094685709:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            
            if emoji == '🎊':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589865180430458))
            elif emoji == '🧛':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589810314739774))
            elif emoji == '🎤':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589889133838386))
            elif emoji == '🎥':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589809353981962))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 325607843547840522:
            return

        if payload.member.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 757601724122005616:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 758135039094685709:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            
            if emoji == '🎊':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589865180430458))
            elif emoji == '🧛':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589810314739774))
            elif emoji == '🎤':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589889133838386))
            elif emoji == '🎥':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589809353981962))

    @commands.command()
    async def coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 577511138032484360:
          return

      if member == None:
        member = ctx.author

      if coins.count_documents({"guild": ctx.guild.id, "id": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{member.mention}, на вашем счету `0` коинов**', colour = 0xFB9E14))

      else:
        return await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{member.mention}, на вашем счету `{coins.find_one({"guild": ctx.guild.id, "id": member.id})["coins"]}` коинов**', colour = 0xFB9E14))

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addcoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 577511138032484360:
          return
      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите пользователя**', colour = 0xFB9E14), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите кол-во добавляемых {pb}**', colour = 0xFB9E14), delete_after = 5)

      if coins.count_documents({"guild": ctx.guild.id, "id": member.id}) == 0:
        a = addbt(ctx.guild.id, member, amount)
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.name}, вы добавили пользователю {member.mention} `{amount}` {pb}.\nЕго баланс: `{a}` коинов**', colour = 0xFB9E14))
      else:
        a = addbt(ctx.guild.id, member, amount)
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.name}, вы добавили пользователю {member.mention} `{amount}` {pb}.\nЕго баланс: `{a}` коинов**', colour = 0xFB9E14))

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def removecoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 577511138032484360:
          return
      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите пользователя**', colour = 0xFB9E14), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите кол-во убираемых {pb}**', colour = 0xFB9E14), delete_after = 5)
      
      a = proverka(ctx.guild.id, member, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.name}, пользователь не имеет такого кол-ва {pb}!**', colour = 0xFB9E14))
      else:
        bal = rebt(ctx.guild.id, member, amount)
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.name}, вы удалили у пользователя {member.mention} `{amount}` {pb}.\nЕго баланс: `{bal}` коинов**', colour = 0xFB9E14))    

    @commands.command()
    async def pay(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 577511138032484360:
          return

      if ctx.channel.id == 756183285188788306:
        return await ctx.message.delete()

      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите пользователя**', colour = 0xFB9E14), delete_after = 5)
      
      if member == ctx.author or member.bot:
        return

      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите сумму {pb} которую нужно передать!**', colour = 0xFB9E14), delete_after = 5)

      if amount <= 0:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, указан неверный аргумент!**', colour = 0xFB9E14), delete_after = 5)


      a = proverka(ctx.guild.id, ctx.author, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.mention}, Вы не можете передать такую сумму!**', colour = 0xFB9E14))

      else:
        bal = addbt(ctx.guild.id, member, amount)
        bal2 = rebt(ctx.guild.id, ctx.author, amount)
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.name}, Вы передали пользователю {member.mention} `{amount}` {pb}.\nЕго баланс: `{bal}` коинов\nВаш баланс: `{bal2}` коинов**', colour = 0xFB9E14))
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def casino(self, ctx, amount : int = None):
      if not ctx.guild.id == 577511138032484360:
        return

      if not ctx.channel.id == 756183285188788306:
        await ctx.message.delete()
        return await ctx.send(embed = discord.Embed(description = f'**Команда `/casino` доступна только в канале <#756183285188788306>**', colour = 0xFB9E14), delete_after = 5)
        
      if amount == None:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите кол-во {pb} которое необходимо поставить!**', colour = 0xFB9E14), delete_after = 5)

      if amount <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, неверный аргумент!**', colour = 0xFB9E14), delete_after = 5)

      a = proverka(ctx.guild.id, ctx.author, amount)
      if a == 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.mention}, Вы не можете сделать такую ставку!**', colour = 0xFB9E14))
      else:
        await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.name}, что же нам выпадет...**', colour = 0xFB9E14), delete_after = 5)
        a = random.randint(1, 2)
        if a == 1:
          await asyncio.sleep(5)
          bal = rebt(ctx.guild.id, ctx.author, amount)
          await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.mention}, к сожалению, вы проиграли!\nТеперь Ваш баланс составляет: `{bal}` коинов!**', colour = 0xFB9E14))
        if a == 2:
          af = random.choices([1, 2, 3, 4], weights=[80, 15, 5, 0.1])[0]
          if af == 1:
            text = 'Вам повезло, вы удвоили свою ставку!'
          elif af == 2:
            amount *= 5
            text = 'Ничего себе, Вы на столько везучий, что увеличили свою ставку в 5 раз!'
          elif af == 3:
            amount *= 10
            text = 'ВООООООООУ!!! Вам очень сильно повезло и фортуна увеличила вашу ставку в 10 раз!'
          elif af == 4:
            amount *= 100
            text = f'Я просто промолчу.... Этот счастливчик сорвал СУПЕР КУШ и умножил свою ставку В СТО РАЗ!!! Он получил целых `{amount}` коинов!'
          await asyncio.sleep(5)
          f = amount
          bal = addbt(ctx.guild.id, ctx.author, f)
          return await ctx.send(embed = discord.Embed(title = 'Система {pb}', description = f'**{ctx.author.mention}, {text}\nТеперь Ваш баланс составляет: `{bal}` коинов!**', colour = 0xFB9E14))
            
    @commands.Cog.listener()
    async def on_message(self, ctx):
      if ctx.guild == None:
        return
        
      if not ctx.guild.id == 577511138032484360:
          return
      global mas

      if ctx.guild == None:
        return

      if not ctx.guild.id == 577511138032484360:
        return

      ath2 = re.findall(r'\w*', ctx.content.lower())

      rekl = ['http', 'https', 'www', '.ru', '.com', '.xxx']
      for i in ath2:
        if i in rekl:
          if not 'rodina' in ath2 and not 'hxa7jmt' in ath2:
            await ctx.delete()
            return await ctx.channel.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ваше сообщение было удалено по подозрению в рекламе.**", colour = 0xFB9E14), delete_after = 10)



      if discord.utils.get(ctx.guild.roles, id = 736949012065943592) in ctx.author.roles:
        return

      if ctx.content.startswith('/') or ctx.content.startswith('!') or ctx.content.startswith('+'):
        return

      if ctx.author.bot:
        return

      st = 0
      if len(list(ctx.content)) >= 2:
        a = addbs(ctx.author.id, "messages")
        if a == 1000:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 1000 сообщений!` 🎉\nВам добавлен бонус в размере 5000 коинов <3**', colour = 0xFB9E14))
          st = 5000
        if a == 3000:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 3000 сообщений!` 🎉\nВам добавлен бонус в размере 10000 коинов <3**', colour = 0xFB9E14))
          st = 10000
        

        if st > 0:
          addbt(ctx.guild.id, ctx.author, st)


        
      role_registr = [ 'роль', 'роли', 'дайте роль', 'хочу роль', 'роль дайте', 'выдайте роль', '-роль', 'Роль', 'Роли', 'Дайте роль', 'Хочу роль', 'Роль дайте', 'Выдайте роль', '-Роль', '!Роль', '!роль' ]
      if ctx.channel.id == 756183285188788306:
        if not ctx.content == '/casino' and not ctx.content.lower() in role_registr:
          return await ctx.delete()

      a = proc(len(list(ctx.content)))
      addbt(ctx.guild.id, ctx.author, a)

    @commands.command()
    async def user(self, ctx, member: discord.Member = None):

      CHAS = {
        1: '1 час ночи',
        2: '2 часа ночи',
        3: '3 часа ночи',
        4: '4 часа ночи',
        5: '5 часов утра',
        6: '6 часов утра',
        7: '7 часов утра',
        8: '8 часов утра',
        9: '9 часов утра',
        10: '10 часов утра',
        11: '11 часов утра',
        12: '12 часов дня',
        13: '1 час дня',
        14: '2 часа дня',
        15: '3 часа дня',
        16: '4 часа дня',
        17: '5 часов вечера',
        18: '6 часов вечера',
        19: '7 часов вечера',
        20: '8 часов вечера',
        21: '9 часов вечера',
        22: '10 часов вечера',
        23: '11 часов вечера',
        00: 'первом часу ночи'
      }

      FCH = {
        1: 'Января', 
        2: 'Февраля', 
        3: 'Марта', 
        4: 'Апреля', 
        5: 'Мая', 
        6: 'Июня', 
        7: 'Июля', 
        8: 'Августа', 
        9: 'Сентября', 
        10: 'Октября', 
        11: 'Ноября',
        12: 'Декабря',
      }
      
      accept = [451410256736550918]
      rolid = [577524866320826368, 577524754798346261, 577524969051914262, 577523815890944007, 577525668061904899]
      member = ctx.author if not member else member
      roles = [ ]
      
      if not len(member.roles) == 1:
          f = 0
          for i in member.roles:
              if not i.id == ctx.guild.default_role.id:
                  f += 1
                  s = len(member.roles) - f
                  roles.append(f'`{s}.` <@&{i.id}>\n')
      embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)

      embed.set_author(name = f"🍀 Информация о пользователе - {member}")
      embed.set_thumbnail(url = member.avatar_url)

      embed.add_field(name = "🔻 `Имя`", value = f'{member.display_name}', inline = False)
      if member.id == 646573856785694721 or member.id in accept:
          embed.add_field(name = f'♦ `Аккаунт`', value = f'{member.mention} <:verefication:733973297339039874> | Является оффициально подтверждённым', inline = False)
      else:
          embed.add_field(name = f'♦ `Аккаунт`', value = member.mention, inline = False)
      embed.add_field(name = "🔹 `ID`", value = f'{member.id}', inline = False)

      ath = re.split(r'\W+', str(member.created_at))

      vr = CHAS[int(ath[3])]
      fo = re.split(r'\W+', str(vr))

      embed.add_field(name = "⌚ `Зарегистрирован`", value = f'{ath[2]} {FCH[int(ath[1])]} {ath[0]} года в {fo[0]} {fo[1]} {fo[2]}', inline = False)

      ath = re.split(r'\W+', str(member.joined_at))

      vr = CHAS[int(ath[3])]
      fo = re.split(r'\W+', str(vr))

      embed.add_field(name = "⌚ `Вошел на сервер`", value = f'{ath[2]} {FCH[int(ath[1])]} {ath[0]} года в {fo[0]} {fo[1]} {fo[2]}', inline = False)

      if ctx.guild.id == 577511138032484360:
        if users.count_documents({"guild": ctx.guild.id, "id": member.id}) == 1:
          if users.find_one({"guild": ctx.guild.id, "id": member.id})["messages"] < 0:
            msgs = 0
          else:
            msgs = users.find_one({"guild": ctx.guild.id, "id": member.id})["messages"]
          
          if users.find_one({"guild": ctx.guild.id, "id": member.id})["vsv"] < 0:
            voices = f'00:00:00'
          else:
            seconds = users.find_one({"guild": ctx.guild.id, "id": member.id})["vsv"]
            seconds = seconds % (24 * 3600)
            days = seconds // (60 * 60 * 24)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            voices = f'{days} дн. {hours} ч. {minutes} мин. {seconds} cек'
        else:
          voices = f'00:00:00'
          msgs = 0
  
        embed.add_field(name = '🗣 Голосовая активность', value = f"`{voices}`", inline = False)
          
        embed.add_field(name = '✏ Всего сообщений', value = f'`Сообщений в чатах:` **{msgs}**')

        achive = []
        if msgs >= 1000:
          achive.append('[✅] Написать `1000` сообщений\n')
        else:
          achive.append('[❎] Написать `1000` сообщений\n')

        if msgs >= 3000:
          achive.append('[✅] Написать `3000` сообщений\n')
        else:
          achive.append('[❎] Написать `3000` сообщений\n')

        str_a = ''.join(achive)
        embed.add_field(name = '💰 `Достижения`', value = f'**{str_a}**')

      if member.bot:
        embed.add_field(name = "🔸 Информация", value = '`Этот аккаунт является Discord-Ботом!`', inline = False)
        return await ctx.send(embed = embed)

      if len(member.roles) <= 1:
        embed.add_field(name = f"📊 `Роли({len(roles)})`", value = '**Ролей нет.**', inline = False)
      elif len(member.roles) > 1:
        roles1 = roles[::-1]
        embed.add_field(name = f"📊 `Роли({len(roles)})`", value = "".join(roles1), inline = False)
        embed.add_field(name = "🏮 `Высшая роль`", value = member.top_role.mention, inline = False)

      teh1 = discord.utils.get(ctx.guild.roles, id = 703270075666268160)
      if teh1 in member.roles:
        embed.add_field(name = "🏆 Support", value = f'`Данный пользователь является является агентом технической поддержки` {teh1.mention}', inline = False)

      bust = discord.utils.get(ctx.guild.roles, id = 752179518168367176)
      if bust in member.roles:
        embed.add_field(name = "❤ Follow", value = f'`Данный пользователь поддержал данный Discord-Сервер.`', inline = False)
      
      if member.top_role.id in rolid:          
        embed.add_field(name = "📌 Importent Persone", value = f'`Данный пользователь является администратором проекта.`', inline = False)

      stadm = [577525590769532938, 577530456870748171, 577526148330815498]
      if member.top_role.id in stadm:
        embed.add_field(name = "<:owner:733973554206343168> Senior Administrator", value = f'`Данный пользователь находится в составе старшей администрации проекта.`', inline = False)

      embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
      embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
      await ctx.send(embed = embed)

    @commands.command(aliases = ['теннис'])
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def tennis(self, ctx, member: discord.Member = None, stavka : int = None):
      global tens
      stor = 0
      if not ctx.guild.id == 577511138032484360:
          return

      await ctx.message.delete()

      if not member:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя с которым хотите начать игру!\n/tennis @Пользователь#1234 [сумма]```', delete_after = 5)

      if not stavka:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Укажите ставку на которую хотите сыграть!\n/tennis @Пользователь#1234 [сумма]```', delete_after = 5)

      if ctx.author.id in tens:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Вы находитесь в активной игре!```', delete_after = 5)

      if member.id in tens:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Этот пользователь находится в активной игре!```', delete_after = 5)

      if member == ctx.author:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Нельзя играть с самим собой!```', delete_after = 3)

      if stavka <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Нельзя выбрать ставку меньше или равной нулю!```', delete_after = 3)

      one = proverka(ctx.author, stavka)
      two = proverka(member, stavka)

      if not one == 1 or not two == 1:
        if not one == 1 and not two == 1:
          ctx.command.reset_cooldown(ctx)
          return await ctx.send(f'{ctx.author.mention}, ```Никто из участников не имеет нужной суммы!```', delete_after = 5)

        if not one == 1:
          ctx.command.reset_cooldown(ctx)
          return await ctx.send(f'{ctx.author.mention}, ```Вы не имеете нужной суммы!```', delete_after = 5)

        if not two == 1:
          ctx.command.reset_cooldown(ctx)
          return await ctx.send(f'{ctx.author.mention}, ```Выбранный пользователь не имеет нужно суммы```', delete_after = 5)

      try:
        await ctx.author.send('+', delete_after = 1)
      except discord.Forbidden:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Откройте личные сообщения в настройках конфиденциальности для того что бы начать игру!```', delete_after = 5)

      try:
        mes = await member.send(f'`[ZAPROS]` `Здравствуйте` {member.mention}! `Пользователь {ctx.author.display_name} хочет сыграть с вами в теннис.\nСтавка на игру: {stavka} коинов!\nДля того что бы принять его предложение нажмите на` 🔋 `под этим сообщением.`\n`В противном случае проигнорируйте это сообщение!`')
        await mes.add_reaction('🔋')
        await ctx.send(embed = discord.Embed(description = f'**Пользователю {member.name} было отправлено предложение сыграть.\nНа подтверждение ему даётся 30 секунд.**', colour = 0xFB9E14), delete_after = 10)
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == member and react.emoji == '🔋')
        except Exception:
          await mes.delete()
          return await ctx.send(f'{ctx.author.mention}, ```Пользователь проигнорировал Ваше предложение!```', delete_after = 15)
        else:
          await mes.delete()
          tens.append(member.id)
          tens.append(ctx.author.id)
          embed = discord.Embed(title = 'Игра в теннис', description = f'**Что это вообще такое? - Возник у вас вопрос.\nЭто увеселительная игра, в которой всё решает ваша удача и знание вашего оппонента!\nВ личные сообщения, бот присылает Вам сообщение, в котором вы должны будете выбрать, правую или левую сторону, так же можно ударить по середине!\nУсловно, это выбор стороны в которую Ваш соперник отправил мяч. Думать и отвечать необходимо достаточно быстро, так как на выбор Вам даётся ровно 15 секунд!\nЕсли в течении этого времени не будет выбрана сторона, Вы автоматом становитесь проигравшим. Для того что бы победить, Вам необходимо первым заработать 10 очков.\nКаждый гол даёт Вам одно очко, если Вы отбиваете мяч, тогда два.\n\nЖелаем Вам приятной игры, начало через 20 секунд. Первым бросает {member.display_name}, гости начинают!**', colour = 0xFB9E14)
          embed.set_author(name = 'Теннис - Rodina RP | Восточный Округ', icon_url = ctx.guild.icon_url)
          embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
          embed.set_thumbnail(url = ctx.guild.icon_url)
          try:
            await member.send(embed = embed, delete_after = 20)
          except:
            tens.remove(member.id)
            tens.remove(ctx.author.id)
            rebt(member, stavka)
            addbt(ctx.guild.id, ctx.author, stavka)
            return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)
          try:
            await ctx.author.send(embed = embed, delete_after = 20)
          except:
            tens.remove(member.id)
            tens.remove(ctx.author.id)
            addbt(member, stavka)
            rebt(ctx.author, stavka)
            return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)
          
          await asyncio.sleep(20)
          r_list = ['⬅', '⬆', '➡']
          with open("cogs/tennis.json", "r") as file:
              data = json.load(file)
          if str(ctx.guild.id) not in data.keys():
            data[str(ctx.guild.id)] = {}

    
          data[str(ctx.guild.id)][str(ctx.author.id)] = 0
          data[str(ctx.guild.id)][str(member.id)] = 0
          with open("cogs/tennis.json", "w") as file:
              json.dump(data, file, indent = 4)
          st = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
          for i in st:   
            with open("cogs/tennis.json", "r") as file:
              data = json.load(file)

            try:
              msg = await member.send(embed = discord.Embed(description = f'**{member.mention}, Ваш ход!\nВыбирайте в какую сторону вы ударите!\n\n> `Нажмите` ⬅ `для удара в левую сторону`\n> `Нажав на` ⬆ `Вы отправите мяч в середину.`\n> `Для удара в правую сторону используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
              for f in r_list:
                await msg.add_reaction(f)
              try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == member and react.emoji in r_list)
              except Exception:
                await msg.delete()
                data[str(ctx.guild.id)][str(member.id)] = 0
                data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                with open("cogs/tennis.json", "w") as file:
                  json.dump(data, file, indent = 4)
                tens.remove(member.id)
                tens.remove(ctx.author.id)
                rebt(member, stavka)
                addbt(ctx.guild.id, ctx.author, stavka)
                try:
                  await member.send(f'{member.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                except:
                  pass
              
                try:
                  return await ctx.author.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {member.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                except:
                  return
              else:
                await msg.delete()
                if str(react.emoji) == r_list[0]:
                  stor = 'левую'
                  txt = 'Вы выбрали `левую` сторону, ожидайте дальнейшей информации!'
                elif str(react.emoji) == r_list[2]:
                  stor = 'правую'
                  txt = 'Вы выбрали `правую` сторону, ожидайте дальнейшей информации!'
                elif str(react.emoji) == r_list[1]:
                  stor = 'середине'
                  txt = 'Вы решили ударить по `середине`, ожидайте дальнейшей информации!'

                await member.send(embed = discord.Embed(description = f'**{txt}**', colour = 0xFB9E14), delete_after = 5)
                if ctx.author.id == 646573856785694721:
                  await ctx.author.send(f'`Выбор соперника: {stor}`', delete_after = 5)
                try:
                  msg = await ctx.author.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Ваш соперник сделал ход!\nВыбирайте в какую сторону вы поставите ракетку, что бы отбить его подачу!\n\n`Нажмите` ⬅ `для выбора левой стороны`\n> `Нажав на` ⬆ `Вы отправите мяч в середину`\n`Для выбора правой стороны используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
                  for f in r_list:
                    await msg.add_reaction(f)
                  try:
                    react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in r_list)
                  except Exception:
                    await msg.delete()
                    data[str(ctx.guild.id)][str(member.id)] = 0
                    data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                    tens.remove(member.id)
                    tens.remove(ctx.author.id)
                    rebt(member, stavka)
                    addbt(ctx.guild.id, ctx.author, stavka)
                    try:
                      await member.send(f'{member.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                    except:
                      pass

                    try:
                      return await ctx.author.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {member.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                    except:
                      pass
                  else:
                    await msg.delete()
                    if str(react.emoji) == r_list[0]:
                      a = 'левую'
                    elif str(react.emoji) == r_list[2]:
                      a = 'правую'
                    elif str(react.emoji) == r_list[1]:
                      a = 'середине'

                    if a == stor:
                      data[str(ctx.guild.id)][str(ctx.author.id)] += 2
                      g2 = data[str(ctx.guild.id)][str(member.id)]
                      g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                      text = f'{ctx.author.display_name} смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                    else:
                      data[str(ctx.guild.id)][str(member.id)] += 1
                      g2 = data[str(ctx.guild.id)][str(member.id)]
                      g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                      text = f'{ctx.author.display_name} не смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                    try:
                      await member.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                    except:
                      pass
                    try:
                      await ctx.author.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                    except:
                      pass
                    
                    g2 = data[str(ctx.guild.id)][str(member.id)]
                    g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                    if g2 >= 10:                           
                      tens.remove(member.id)
                      tens.remove(ctx.author.id)
                      data[str(ctx.guild.id)][str(member.id)] = 0
                      data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                      addbt(member, stavka)
                      rebt(ctx.author, stavka)
                      with open("cogs/tennis.json", "w") as file:
                        json.dump(data, file, indent = 4)
                      try:
                        await member.send(f'{member.mention}, ```Вы выиграли эту партию у игрока {ctx.author.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                      except:
                        pass

                      try:
                        return await ctx.author.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {member.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                      except:
                        return
                    
                    if g1 >= 10:
                      tens.remove(member.id)
                      tens.remove(ctx.author.id)
                      data[str(ctx.guild.id)][str(member.id)] = 0
                      data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                      rebt(member, stavka)
                      addbt(ctx.guild.id, ctx.author, stavka)
                      with open("cogs/tennis.json", "w") as file:
                        json.dump(data, file, indent = 4)
                      try:
                        await ctx.author.send(f'{ctx.author.mention}, ```Вы выиграли эту партию у игрока {member.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                      except:
                        pass

                      try:
                        return await member.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {ctx.author.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                      except:
                        return
                    try:
                      msg = await ctx.author.send(embed = discord.Embed(description = f'**{ctx.author.mention}, теперь Ваш ход!\nВыбирайте в какую сторону вы ударите!\n\n> `Нажмите` ⬅ `для удара в левую сторону`\n> `Нажав на` ⬆ `Вы отправите мяч в середину`\n> `Для удара в правую сторону используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
                      for f in r_list:
                        await msg.add_reaction(f)                 
                      try:
                        react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in r_list)                      
                      except Exception:
                        await msg.delete()
                        data[str(ctx.guild.id)][str(member.id)] = 0
                        data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                        tens.remove(member.id)
                        tens.remove(ctx.author.id)
                        addbt(member, stavka)
                        rebt(ctx.author, stavka)
                        with open("cogs/tennis.json", "w") as file:
                            json.dump(data, file, indent = 4)
                        try:
                          await ctx.author.send(f'{ctx.author.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                        except:
                          pass
                        try:
                          return await member.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {ctx.author.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                        except:
                          return
                      
                      else:
                        await msg.delete()
                        if str(react.emoji) == r_list[0]:
                          stor = 'левую'
                          txt = 'Вы выбрали `левую` сторону, ожидайте дальнейшей информации!'
                        elif str(react.emoji) == r_list[2]:
                          stor = 'правую'
                          txt = 'Вы выбрали `правую` сторону, ожидайте дальнейшей информации!'
                        elif str(react.emoji) == r_list[1]:
                          stor = 'середине'
                          txt = 'Вы решили ударить по `середине`, ожидайте дальнейшей информации!'

                        await ctx.author.send(embed = discord.Embed(description = f'**{txt}**', colour = 0xFB9E14), delete_after = 5)
                        if member.id == 646573856785694721: 
                          await member.send(f'`Выбор соперника: {stor}`', delete_after = 5)
                        try:
                          msg = await member.send(embed = discord.Embed(description = f'**{member.mention}, Ваш соперник сделал ход!\nВыбирайте в какую сторону вы поставите ракетку, что бы отбить его подачу!\n\n`Нажмите` ⬅ `для выбора левой стороны`\n> `Нажав на` ⬆ `Вы отправите мяч в середину.`\n`Для выбора правой стороны используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
                          for f in r_list:
                            await msg.add_reaction(f)
                          try:
                            react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == member and react.emoji in r_list)
                          except Exception:
                            await msg.delete()
                            data[str(ctx.guild.id)][str(member.id)] = 0
                            data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                            tens.remove(member.id)
                            tens.remove(ctx.author.id)
                            rebt(member, stavka)
                            addbt(ctx.guild.id, ctx.author, stavka)
                            with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)
                            try:
                              await member.send(f'{member.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                            except:
                              pass

                            try:
                              return await ctx.author.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {member.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                            except:
                              return
                          else:
                            await msg.delete()
                            if str(react.emoji) == r_list[0]:
                              a = 'левую'
                            elif str(react.emoji) == r_list[2]:
                              a = 'правую'
                            elif str(react.emoji) == r_list[1]:
                              a = 'середине'

                            if a == stor:
                              data[str(ctx.guild.id)][str(member.id)] += 2
                              g2 = data[str(ctx.guild.id)][str(member.id)]
                              g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                              text = f'{member.display_name} смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                            else:
                              data[str(ctx.guild.id)][str(ctx.author.id)] += 1
                              g2 = data[str(ctx.guild.id)][str(member.id)]
                              g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                              text = f'{member.display_name} не смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                            try:
                              await member.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                            except:
                              pass
                            try:
                              await ctx.author.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                            except:
                              pass

                            g2 = data[str(ctx.guild.id)][str(member.id)]
                            g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                            if g2 >= 10:                           
                              tens.remove(member.id)
                              tens.remove(ctx.author.id)
                              addbt(member, stavka)
                              rebt(ctx.author, stavka)
                              data[str(ctx.guild.id)][str(member.id)] = 0
                              data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                              with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)
                              try:
                                await member.send(f'{member.mention}, ```Вы выиграли эту партию у игрока {ctx.author.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                              except:
                                pass

                              try:
                                return await ctx.author.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {member.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                              except:
                                pass
                            
                            if g1 >= 10:
                              tens.remove(member.id)
                              tens.remove(ctx.author.id)
                              rebt(member, stavka)
                              addbt(ctx.guild.id, ctx.author, stavka)
                              data[str(ctx.guild.id)][str(member.id)] = 0
                              data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                              with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)

                              try:
                                await ctx.author.send(f'{ctx.author.mention}, ```Вы выиграли эту партию у игрока {member.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                              except:
                                pass

                              try:
                                return await member.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {ctx.author.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                              except:
                                pass

                            with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)
                        
                        except discord.Forbidden:
                          data[str(ctx.guild.id)][str(member.id)] = 0
                          data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                          tens.remove(member.id)
                          tens.remove(ctx.author.id)
                          with open("cogs/tennis.json", "w") as file:
                              json.dump(data, file, indent = 4)
                          return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)

                    except discord.Forbidden:
                      data[str(ctx.guild.id)][str(member.id)] = 0
                      data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                      tens.remove(member.id)
                      tens.remove(ctx.author.id)
                      with open("cogs/tennis.json", "w") as file:
                          json.dump(data, file, indent = 4)
                      return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)
                
                except discord.Forbidden:
                  data[str(ctx.guild.id)][str(member.id)] = 0
                  data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                  tens.remove(member.id)
                  tens.remove(ctx.author.id)
                  with open("cogs/tennis.json", "w") as file:
                      json.dump(data, file, indent = 4)
                  return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)

            except discord.Forbidden:
              data[str(ctx.guild.id)][str(member.id)] = 0
              data[str(ctx.guild.id)][str(ctx.author.id)] = 0
              tens.remove(member.id)
              tens.remove(ctx.author.id)
              with open("cogs/tennis.json", "w") as file:
                  json.dump(data, file, indent = 4)
              return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)

      except discord.Forbidden:
        ctx.command.reset_cooldown(ctx)
        with open("cogs/tennis.json", "w") as file:
            json.dump(data, file, indent = 4)
        return await ctx.send(f'{ctx.author.mention}, ```Выбранный пользователь ограничил отправку личных сообщений, я не могу отправить ему запрос на подтверждение!```', delete_after = 5)

    @commands.command(aliases = ['обнулить', 'очистить'])
    @commands.has_permissions(administrator = True)
    async def reset_coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 577511138032484360:
        return

      if ctx.channel.id == 756183285188788306:
        return await ctx.message.delete()

      await ctx.message.delete()
      if not member:
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя!```', delete_after = 5)

      if ctx.author.top_role.position <= member.top_role.position:
        return

      if coins.count_documents({"guild": ctx.guild.id, "id": member.id}) != 0:
        coins.update_one({"guild": ctx.guild.id, "id": member.id}, {"$set": {"coins": 0}})
      else:
        pass
      channel = self.bot.get_channel(736200220311945256)
      await channel.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил коины пользователю {member.mention}!**', colour = 0xFB9E14, timestamp = ctx.message.created_at))
      return await ctx.send(f'{ctx.author} => {member}', embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил коины пользователю {member.mention}!**', colour = 0xFB9E14))

def setup(bot):
    bot.add_cog(econom(bot))

'''

