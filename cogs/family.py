# -*- encoding: utf-8 -*-

import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time
import os.path
import asyncio
import json
import requests
from pymongo import MongoClient
import difflib

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodinaname"]
dbs = cluster["RodinaBD"]
fam = db["famacoll"]
zapros = db["zaproscoll"]
famuser = db["famuser"]
users = db["users"]
reports = dbs["reports"]


class family(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Rodina 04 | System of Family by kodiknarkotik#5187 - Запущен")
	
	@commands.command(aliases = ['fhelp'])
	async def famhelp(self, ctx):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		await ctx.message.delete()
		name = 'Северный Округ' if ctx.guild.id == 477547500232769536 else 'Восточный Округ'
		if ctx.guild.id == 577511138032484360:
			embed = discord.Embed(title = f'\⛩️ **__Список моих команд:__**', description = f'**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}createfam__** *(создать|fc)* **@user** - Создать семью.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}removefam__** *(удалить|fr)* **[название семьи]** - Удалить семью по названию.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}faminvite__** *(пригласить|finvite)* **@user** - Пригласить пользователя в семью.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}famuninvite__** *(исключить|funinvite)* **@user** - Исключить пользователя из семьи.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}addfamzam__** *(назначить|afz)* **@user** - Назначить пользователя заместителем семьи.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}removefamzam__** *(разжаловать|rfz)* **@user** - Снять пользователя с ранга "Заместитель".\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}faminfo__** *(осемье|finfo)* **[название семьи]** - Узнать информацию о семье.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}fammenu__** *(fmenu)* - Открыть меню управления семьей.\n**__{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}famlist__** *(семьи|flist)* - Список всех семей сервера.')
		else:
			embed = discord.Embed(title = f'{name} | Команды семей', description = f'🔹 **| Список моих команд:**\n> `1.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}createfam`(создать|fc)`** @Пользователь#1234 - Создать семью`[Указать пользователя который будет лидером семьи].`\n> `2.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}removefam`(удалить|fr)`** [название семьи] - Удалить семью по названию.\n> `3.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}faminvite`(пригласить|finvite)`** @Пользователь#1234 - Пригласить пользователя в семью.\n> `4.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}famuninvite`(исключить|funinvite)`** @Пользователь#1234 - Исключить пользователя из семьи.\n> `5.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}addfamzam`(назначить|afz)`** @Пользователь#1234 - Назначить пользователя заместителем семьи.\n> `6.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}removefamzam`(разжаловать|rfz)`** @Пользователь#1234 - Снять пользователя с ранга `"Заместитель"`\n> `7.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}faminfo`(осемье|finfo)`** [название семьи] - Узнать информацию о семье`[Если название не указано, информация о вашей семье].`\n> `8.` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}fammenu`(fmenu)`** - Открыть меню управления семьёй.\n> `9.` **!famlist`(семьи|flist)`** - Список всех семей сервера.')
			embed.set_thumbnail(url = ctx.guild.icon_url)
			embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
			await ctx.send(embed = embed, delete_after = 60)


	@commands.command(aliases = ["создать", "fc"])
	@commands.has_permissions(administrator = True)
	async def createfam(self, ctx, member: discord.Member = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		await ctx.message.delete()
		if member is None:
			return await ctx.send(embed = discord.Embed(description = f'❗ {ctx.author.name}, `вы не указали пользователя, которому будет принадлежать создаваемая семья!`\n\n**Пример использования команды:**\n> `{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}createfam(создать|fc) [@user#1234]`\n-- Я буду знать, что владельцем будущей семьи станет указанный вами пользователь.', color = 0xFB0E14), delete_after = 7)

		if fam.count_documents({"guild": ctx.guild.id, "leaderID": member.id}) > 0:
			return await ctx.send(embed = discord.Embed(description = f'❗ {ctx.author.name}, `указанный пользователь является лидером другой семьи.', color = 0xFB0E14), delete_after = 7)

		if ctx.guild.id == 577511138032484360: # ТОТЯ 
			m = await ctx.send(embed = discord.Embed(title = '\⛩️ **__Заполнение данных:__**', description = f'**Заполните данные:**\n**1.** Владелец семьи: {member.mention}`({member})`\n**2.** Название семьи: *__Не указано__*\n**3.** Название семейной роли: *__Не указано__*\n**4.** Цвет семейной роли: *__Не указано__*\n**5.** Название семейного голосового канала: *__Не указано__*\n\n**__Для начала укажите название семьи__**\nПример: dollar family\nЯ установлю семье такое название!\n\n**Для того что бы отменить создание семьи введите:** `Отмена`'))
		else:
			m = await ctx.send(embed = discord.Embed(title = 'Заполнение данных', description = f'Для создания семьи, Вам необходимо заполнить некоторые данные, список которых представлен ниже.\n1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **Не указано**\n3. `Название семейной роли:` **Не указано**\n4. `Цвет семейной роли:` **Не указано**\n5. `Название семейного голосового канала:` **Не указано**\n\n**Для начала укажите название семьи**\n> `Пример:` dollar family\n-- Я установлю семье такое название\n\n`Для того что бы отменить создание семьи введите:` **Отмена**'))
		def check(m):
			return m.channel == ctx.channel and m.author == ctx.author
		try:
			msg = await self.bot.wait_for('message', check = check, timeout= 120.0)
		except TimeoutError:
			return await m.delete()
		else:
			await msg.delete()
			if msg.content.lower() == 'отмена':
				return await m.delete() 
			if ctx.guild.id == 577511138032484360: # ТОТЯ 
				await m.edit(embed = discord.Embed(title = '\⛩️ **__Заполнение данных:__**', description = f'**Заполните данные:**\n**1.** Владелец семьи: {member.mention}`({member})`\n**2.** Название семьи: **{msg.content}**\n**3.** Название семейной роли: *__Не указано__*\n**4.** Цвет семейной роли: *__Не указано__*\n**5.** Название семейного голосового канала: *__Не указано__*\n\n**__Теперь установите название семейной роли__**\nПример: {msg.content}\nЯ установлю семье такое название!\n\n**Для того что бы отменить создание семьи введите:** `Отмена`'))
				m1 = await ctx.send("**`Напишите в чат название семейной роли:`**", embed = discord.Embed(description = f'> **Пример:** `{msg.content} role`\n-- Я установлю `{msg.content} role` названием семейной роли\n\n> `Для установки стандартного названия:` **-**\n-- Я установлю `название семьи` в название роли.\n\nЧто бы отменить создание семьи используйте: `Отмена`'))
			else:
				await m.edit(embed = discord.Embed(title = 'Заполнение данных', description = f'Получил Ваш ответ, очень оригинально! Продолжайте заполнять данные!\n1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **{msg.content}**\n3. `Название семейной роли:` **Не указано**\n4. `Цвет семейной роли:` **Не указано**\n5. `Название семейного голосового канала:` **Не указано**\n\n**Теперь установите название семейной роли**\n> **Пример:** `{msg.content} role`\n-- Я установлю `{msg.content} role` названием семейной роли\n\n> `Для установки стандартного названия:` **-**\n-- Я установлю `название семьи` в название роли.\n\n`Для того что бы отменить создание семьи введите:` **Отмена**'))
				m1 = await ctx.send("**`Напишите в чат название семейной роли:`**", embed = discord.Embed(description = f'> **Пример:** `{msg.content} role`\n-- Я установлю `{msg.content} role` названием семейной роли\n\n> `Для установки стандартного названия:` **-**\n-- Я установлю `название семьи` в название роли.\n\nЧто бы отменить создание семьи используйте: `Отмена`'))
			def check(m):
				return m.channel == ctx.channel and m.author == ctx.author
			try:
				msg1 = await self.bot.wait_for('message', check = check, timeout= 120.0)
			except TimeoutError:
				await m.delete()
				return await m1.delete()
			else:
				await msg1.delete()
				await m1.delete()
				if msg1.content.lower() == 'отмена':
					return await m.delete()
				frolename = f'{msg.content} role' if msg1.content == '-' else msg.content
				if ctx.guild.id == 577511138032484360: # ТОТЯ
					await m.edit(embed = discord.Embed(title = '\⛩️ **__Заполнение данных:__**', description = f'**Заполните данные:**\n**1.** Владелец семьи: {member.mention}`({member})`\n**2.** Название семьи: **__{msg.content}__**\n**3.** Название семейной роли: *__{frolename}__*\n**4.** Цвет семейной роли: *__Не указано__*\n**5.** Название семейного голосового канала: *__Не указано__*\n\n**__Теперь установите цвет для семейной роли__**\nНапример: #2f3236\n\n**Чтобы отменить создание семьи используйте:** `Отмена`'))
					m9 = await ctx.send(embed = discord.Embed(title = '\⛩️ **__Цвет семейной роли:__**', description = 'Чтобы установить цвет для роли, укажите **hex color**\nНапример: #2f3236\n\n**Чтобы отменить создание семьи используйте:** `Отмена`'))
				else:
					await m.edit(embed = discord.Embed(title = 'Заполнение данных', description = f'Понял - принял, обработал. Давайте дальше!\n1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **{msg.content}**\n3. `Название семейной роли:` **{frolename}**\n4. `Цвет семейной роли:` **Не указано**\n5. `Название семейного голосового канала:` **Не указано**\n\n**Теперь установите цвет для семейной роли**\n> **Пример:** `Синий`\n-- Я установлю `синий` цвет для семейной роли.\n\n**Доступные цвета:** `Белый, Чёрный, Голубой, Синий, Бирюзовый, Красный, Жёлтый, Оранжевый, Розовый, Фиолетовый, Пурпурный, Зелёный, Лаймовый`\n\n> `Для установки стандартного цвета:`   **-**\n-- Я установлю `белый` цвет для семейной роли.\n\n`Для того что бы отменить создание семьи введите:` **Отмена**'))
					m9 = await ctx.send("`Напишите в чат название цвета для семейной роли`", embed = discord.Embed(description = '> **Пример:** `Синий`\n-- Я установлю `синий` цвет для семейной роли.\n\n**Доступные цвета:** `Белый, Чёрный, Голубой, Синий, Бирюзовый, Красный, Жёлтый, Оранжевый, Розовый, Фиолетовый, Пурпурный, Зелёный, Лаймовый`\n\n> `Для установки стандартного цвета:`   **-**\n-- Я установлю `белый` цвет для семейной роли.\n\nЧто бы отменить создание семьи используйте: `Отмена`'))
				def check(m):
					return m.channel == ctx.channel and m.author == ctx.author
				try:
					msg9 = await self.bot.wait_for('message', check = check, timeout= 120.0)
				except TimeoutError:
					await m.delete()
					return await m9.delete()
				else:
					if ctx.guild.id == 577511138032484360: # ТОТЯ 
						if not '#' in msg9.content: 
							await m9.delete()
							await m.delete()
							return await ctx.send(embed = discord.Embed(title = '\⛩️ **__Произошла ошибка__**', description = 'Чтобы установить цвет для роли, укажите **hex color**\nНапример: #2f3236\n\n**Начните создание семьи заново.**'), delete_after = 10)
						hexc = "#FFFFFF" if msg9.content == '-' else msg9.content
						fcolor = hexc
					else:
						fcolor = "Белый" if msg9.content == '-' else msg9.content
						colors = {"белый": 0xFFFFFF, "чёрный": 0x000000, "черный": 0x000000, "голубой": 0x6495ED, "синий": 0x0000FF, "бирюзовый": 0x1df5c3, "красный": 0xFF0000, "жёлтый": 0xFFFF00, "желтный": 0xFFFF00, "розовый": 0xFF00FF, "фиолетовый": 0xEE82EE, "пурпурный": 0xA020F0, "оранжевый": 0xFFA500, "зелёный": 0x00FF00, "зеленый": 0x00FF00, "лаймовый": 0x32CD32}
						eq = colors.get(fcolor.lower(), None)
						hexc = 0xFFFFFF if not eq else colors[fcolor.lower()]
					await msg9.delete()
					await m9.delete()
					if msg9.content.lower() == 'отмена':
						return await m.delete()
					
					if ctx.guild.id == 577511138032484360: # ТОТЯ 
						fvoice = f'{msg.content}'
					else:
						await m.edit(embed = discord.Embed(title = 'Заполнение данных', description = f'Есть контакт! Продолжайте заполнение.\n1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **{msg.content}**\n3. `Название семейной роли:` **{frolename}**\n4. `Цвет семейной роли:` **{fcolor}**\n5. `Название семейного голосового канала:` **Не указано**\n\n**Теперь установите название семейного голосового канала**\n> **Пример:** `{msg.content} Voice`\n-- Я установлю `"{msg.content} Voice"` названием семейного голосового канала\n\n> `Для установки стандартного названия:`   **-**\n-- Я установлю `название семьи` в название семейного голосового канала.\n\n`Для того что бы отменить создание семьи введите:` **Отмена**'))
						m2 = await ctx.send("**`Напишите название семейного голосового канала:`**", embed = discord.Embed(description = f'> **Пример:** `{msg.content} Voice`\n-- Я установлю `"{msg.content} Voice"` названием семейного голосового канала\n\n> `Для установки стандартного названия:`   **-**\n-- Я установлю `название семьи` в название семейного голосового канала.\n\nЧто бы отменить создание семьи используйте: `Отмена`'))
						def check(m):
							return m.channel == ctx.channel and m.author == ctx.author
						try:
							msg2 = await self.bot.wait_for('message', check = check, timeout= 120.0)
						except TimeoutError:
							await m.delete()
							return await m2.delete()
						else:
							await msg2.delete()
							fvoice = f'{msg.content} Voice' if msg2.content == '-' else msg2.content
							await m2.delete()
							if msg2.content.lower() == 'отмена':
								return await m.delete()

					await m.delete()
					if ctx.guild.id == 577511138032484360: # ТОТЯ 
						m4 = await ctx.send(embed = discord.Embed(title = '\⛩️ **__Проверка валидности данных__:**', description = f'Отлично! Все данные заполнены!\nПроверьте правильность заполнения и выберите дальнейшие действия\n\n**1.** Владелец семьи: **__{member.mention}`({member})__**\n**2.** Название семьи: **__{msg.content}__**\n**3.** Название семейной роли: **__{frolename}__**\n**4.** Цвет семейной роли: **__{fcolor}__**\n**5.** Название семейного голосового канала: **__{fvoice}__**\n\n**Для того что бы отменить создание семьи введите:** `Отмена/-`\n**Для подтверждения создания семьи введите:** `Да/+`'))
					else:
						m4 = await ctx.send(embed = discord.Embed(title = 'Проверка валидности данных', description = f'Отлично! Все данные заполнены!\nПроверьте правильность их заполнения и выберите дальнейшие действия\n\n1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **{msg.content}**\n3. `Название семейной роли:` **{frolename}**\n4. `Цвет семейной роли:` **{fcolor}**\n5. `Название семейного голосового канала:` **{fvoice}**\n\n`Для того что бы отменить создание семьи введите:` **Отмена**/**-**\n`Для подтверждения создания семьи введите:` **Да**/**+**'))
					def check(m):
						return m.channel == ctx.channel and m.author == ctx.author
					try:
						msg4 = await self.bot.wait_for('message', check = check, timeout= 120.0)
					except TimeoutError:
						return await m4.delete()
					else:
						if msg4.content == "+" or msg4.content.lower() == 'да':
							await msg4.delete()
							await m4.delete()
							if ctx.guild.id == 577511138032484360: # ТОТЯ 
								await ctx.send(embed = discord.Embed(title = '\⛩️ **__Информация о созданной семье__:**', description = f'**1.** Владелец семьи: **__{member.mention}`({member})__**\n**2.** Название семьи: **__{msg.content}__**\n**3.** Название семейной роли: **__{frolename}__**\n**4.** Цвет семейной роли: **__{fcolor}__**\n**5.** Название семейного голосового канала: **__{fvoice}__**'), delete_after = 60)
								emb = discord.Embed(title = '\⛩️ **__Информация о созданной семье__:**', description = f'**Администратор {ctx.author.mention}(`{ctx.author}`) создал новую семью**\n\nИнформация о семье:\n**1.** Владелец семьи: **__{member.mention}`({member})__**\n**2.** Название семьи: **__{msg.content}__**\n**3.** Название семейной роли: **__{frolename}__**\n**4.** Цвет семейной роли: **__{fcolor}__**\n**5.** Название семейного голосового канала: **__{fvoice}__**')
							else:
								await ctx.send(f'`[CREATEFAM]` `Семья "{msg.content}" успешно зарегистрирована.`', embed = discord.Embed(title = 'Информация о созданой семье', description = f'1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **{msg.content}**\n3. `Название семейной роли:` **{frolename}**\n4. `Цвет семейной роли:` **{fcolor}**\n5. `Название семейного голосового канала:` **{fvoice}**'), delete_after = 60)
								emb = discord.Embed(title = 'Создана новая семья', description = f'**Администратор {ctx.author.mention}(`{ctx.author}`) создал новую семью**\n\nИнформация о семье:\n1. `Владелец семьи`: {member.mention}`({member})`\n2. `Название семьи:` **{msg.content}**\n3. `Название семейной роли:` **{frolename}**\n4. `Цвет семейной роли:` **{fcolor}**\n5. `Название семейного голосового канала:` **{fvoice}**')
							emb.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
							emb.set_thumbnail(url = ctx.guild.icon_url)
							await self.bot.get_channel(834039427541631016).send(embed = emb)
							name = msg.content
							leader = member.name
							leaderID = member.id
							role = await ctx.guild.create_role(name = f"{frolename}")
							if ctx.guild.id == 577511138032484360: # ТОТЯ 
								hexf = hexc.replace('#', '0x')
								await role.edit(colour = int(hexf, 16))
							else:
								await role.edit(colour = hexc)
							if ctx.guild.id == 577511138032484360: # ТОТЯ 
								await ctx.guild.edit_role_positions(positions = {role: 28})
								channel = await ctx.guild.create_voice_channel(name = fvoice, category = discord.utils.get(ctx.guild.categories, id = 872174625168162916))
								await self.bot.get_channel(872177316070039582).set_permissions(role, view_channel = True, read_message_history = True, read_messages = True)
							else:
								await ctx.guild.edit_role_positions(positions = {role: 18})
								channel = await ctx.guild.create_voice_channel(name = fvoice, category = discord.utils.get(ctx.guild.categories, id = 591642172349218816))
								await self.bot.get_channel(591642627137339433).set_permissions(role, view_channel = True, read_message_history = True, read_messages = True)
							await channel.set_permissions(role, view_channel = True, connect = True, speak = True, use_voice_activation = True)
							fam.insert_one({"id": [member.id, 1, 1], "guild": ctx.guild.id, "name": name, "channel": channel.id, "leader": leader, "leaderID": leaderID,"mem": 5, "zam1": 1, "zam2": 1, "zam3": 1, "zam4": 1, "verf": 0, "rolename": frolename, "roleID": role.id, "memberid": 1, "mesID": 1})
							await member.add_roles(discord.utils.get(ctx.guild.roles, id = role.id))
						else:
							await msg4.delete()
							await m4.edit(embed = discord.Embed(description = f'Вы успешно отказались от создания семьи!'), delete_after = 5)
								

	@commands.command(aliases = ['пригласить', 'finvite'])
	async def faminvite(self, ctx, member: discord.Member = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id}):
			a = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["roleID"]
			rolepr = discord.utils.get(ctx.guild.roles, id = a)
			if member is None:
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка(1)__**", description = f'❌ Возможные причины её возникновения:\n`•` Вы не указали пользовател которому хотите отправить приглашение\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
			if member == ctx.author:
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка(2)__**", description = f'❌ Возможные причины её возникновения:\n`•` Вы указали пользователем самого себя.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
			if fam.find_one({"id": member.id, "guild": ctx.guild.id}):
				role = discord.utils.get(ctx.guild.roles, id = fam.find_one({"id": member.id, "guild": ctx.guild.id})["roleID"])
				if not role in member.roles: 
					mas = [i for i in fam.find_one({"guild": ctx.guild.id, "id": member.id})["id"]]
					mas.remove(member.id)
					mas.append(1)
					if fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam1"] == member.id: p = "zam1"
					elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam2"] == member.id: p = "zam2"
					elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam3"] == member.id: p = "zam3"
					elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam4"] == member.id: p = "zam4"
					fam.update_one({"guild": ctx.guild.id, "leaderID": ctx.author.id}, {"$set": {p: 1, "id": mas}})
				else:
					return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка(3)__**", description = f'❌ Возможные причины её возникновения:\n`•` Вы указали пользователем самого себя.\n`•` Выбранный пользователь является `лидером/заместителем` одной из семей.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
			if rolepr in member.roles:
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка(4)__**", description = f'❌ Возможные причины её возникновения:\n`•` Вы указали пользователем самого себя.\n`•` Выбранный пользователь является участником данной семьи.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
			else:
				fname = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["name"]
				embed = discord.Embed(title = "\⛩️ **__Приглашение в семью__**", description = f"Пользователь {ctx.author.mention}`({ctx.author})` отправил Вам запрос на вступление семью **__{fname}__**\nДля того что бы выбрать один из предложенных вариантов Вам даётся 30 секунд.\n\n\✅ - **__Принять приглашение и вступить в семью__**\n\❌ - **__Отказаться от вступления в семью__**")
				embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
				message = await ctx.send(f'{member.mention}', embed = embed, delete_after = 30.0) 
				await message.add_reaction("✅")
				await message.add_reaction("❌")
				try:
					react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == member and react.emoji in ['✅', '❌'])
				except Exception:
					ctx.command.reset_cooldown(ctx)
					return await message.delete()
				else:
					await message.delete()
					if str(react.emoji) == '✅':
						for b in member.roles:
							if b.id in [i["roleID"] for i in fam.find({"guild": ctx.guild.id})]: await member.remove_roles(b)

						if fam.find_one({"id": member.id, "guild": ctx.guild.id}):
							mas = [i for i in fam.find_one({"guild": ctx.guild.id, "id": member.id})["id"]]
							mas.remove(member.id)
							mas.append(1)
							if fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam1"] == member.id: p = "zam1"
							elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam2"] == member.id: p = "zam2"
							elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam3"] == member.id: p = "zam3"
							elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam4"] == member.id: p = "zam4"
							fam.update_one({"guild": ctx.guild.id, "leaderID": ctx.author.id}, {"$set": {p: 1, "id": mas}})
						embed = discord.Embed(title = "\⛩️ **__Положительно__**", description = f"✅ {ctx.author}, пользователь {member.mention}`({member})` принял Ваше предложение и присоединился к семье **__{fname}__**\n`[Ps]:` В семью начислено **5** очков репутации.")
						embed.set_thumbnail(url = "https://sm.pcmag.com/t/pcmag_au/review/m/microsoft-/microsoft-invite-for-iphone_2td2.1200.jpg")
						embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
						await ctx.send(f'{ctx.author.mention}', embed = embed)
						await member.add_roles(discord.utils.get(ctx.guild.roles, id = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["roleID"]))
						mem = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"]
						fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"mem": mem + 5}})
						fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"memberid": member.id}})
					if str(react.emoji) == '❌': 
						embed = discord.Embed(title = "\⛩️ **__Отрицательно__**", description = f"❌ {ctx.authorn}, к сожалению, пользователь {member.mention}`({member})` отклонил Ваше предложение стать участником семьи **__{fname}__**")
						embed.set_thumbnail(url = "https://sm.pcmag.com/t/pcmag_au/review/m/microsoft-/microsoft-invite-for-iphone_2td2.1200.jpg")
						embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
						return await ctx.send(f'{ctx.author.mention}', embed = embed)
		else:
			await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка(5)__**", description = f'❌ Возможные причины её возникновения:\n`•` У вас не достаточно прав для выполнения данного действия.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)

	@commands.command(aliases = ['исключить', 'funinvite'])
	async def famuninvite(self , ctx, member: discord.Member = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id}):
			if member is None:
				await ctx.send(embed = discord.Embed(title = '\⛩️ **__Произошла ошибка(1)__**', description = '❌ Возможные причины её возникновения:\n`•` Вы не указали пользователя, к которому должна применяться команда.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
				return
			a = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["roleID"]
			rolepr = discord.utils.get(ctx.guild.roles, id = a)

			if member.id == ctx.author.id:
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка(2)__**\n>", description = f'❌ Возможные причины её возникновения:\n`•` Вы указали пользователем самого себя.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)

			if not rolepr in member.roles:
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__(3)**\n>", description = f'❌ Возможные причины её возникновения:\n`•` Выбранный пользователь не является участников Вашей семьи.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
			if member.id == fam.find_one({"id": member.id, "guild": ctx.guild.id}):
				await ctx.send(embed = discord.Embed(title = '\⛩️ **__Произошла ошибка__(4)**', description = f'❌ Возможные причины её возникновения:\n`•` Вы указали пользователем самого себя.\n`•` Выбранный пользователь является `лидером/заместителем` Вашей семьи\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)
				return
			else:
				fname = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["name"]
				embed = discord.Embed(title = '\⛩️ **__Исключение члена семьи__**', description = f'{ctx.author}, Вы действительно хотите выгнать пользователя {member.mention}`({member})` из вашей семьи **__{fname}__**?\n\n✅ - **Исключить**\n❌ - **Отменить действие**')
				embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
				message = await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 30.0)
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
						await member.remove_roles(discord.utils.get(ctx.guild.roles, id = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["roleID"]))
						embed = discord.Embed(title = '\⛩️ **__Исключение члена семьи__**', description = f'✅ {ctx.author}, Вы успешно исключили пользователя {member.mention}`({member})` из вашей семьи **__{fname}__**')
						embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
						await ctx.send(embed = embed)
						if member.id in fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["id"]:
							mas = fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["id"]
							mas.remove(member.id)
							mas.append(1)
							if fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam1"] == member.id: p = "zam1"
							elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam2"] == member.id: p = "zam2"
							elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam3"] == member.id: p = "zam3"
							elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam4"] == member.id: p = "zam4"
							fam.update_one({"guild": ctx.guild.id, "leaderID": ctx.author.id}, {"$set": {p: 1, "id": mas}})
					elif str(react.emoji) == '❌':
						embed = discord.Embed(title = '\⛩️ **__Исключение члена семьи__**', description = f'❌ {ctx.author}, Вы отменили действие.')
						embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
						await ctx.send(f'{ctx.author.mention}', embed = embed, delete_after = 5)
		else:
			await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__(6)**\n>", description = f'❌ Возможные причины её возникновения:\n`•` Вам не доступно использование данной команды.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 10.0)

	@commands.command(aliases = ['осемье', 'finfo'])
	async def faminfo(self, ctx, *, amount: str = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		if amount is None:
			for i in ctx.author.roles:
				if i.id in [i["roleID"] for i in fam.find({"guild": ctx.guild.id})]:
					amount = fam.find_one({"guild": ctx.guild.id, "roleID": i.id})["name"]
					break
		if amount == None:
    			return await ctx.send(embed = discord.Embed(description = f'Не удалось найти указатель семьи.\n**Используйте команду:** !faminfo `[название семьи]`'), delete_after = 7)
		
		else:
			mas = [i["name"] for i in fam.find({"guild": ctx.guild.id})]
			b = 0
			for i in mas:
				if i.count(amount) > b:
					amount = i

		if not fam.count_documents({"guild": ctx.guild.id, "name": amount}) == 0:
			fname = fam.find_one({"name": amount, "guild": ctx.guild.id})["name"]
			leader = fam.find_one({"name": amount, "guild": ctx.guild.id})["leaderID"]
			role1 = fam.find_one({"name": amount, "guild": ctx.guild.id})["roleID"]
			member = fam.find_one({"name": amount, "guild": ctx.guild.id})["memberid"]
			rep = fam.find_one({"name": amount, "guild": ctx.guild.id})["mem"]
			role = discord.utils.get(ctx.guild.roles, id = fam.find_one({"name": amount, "guild": ctx.guild.id})["roleID"])
			embed = discord.Embed(title = "**📢 Информация о семьях Discord'a:**", description = f"**🔥Название семьи:↔ {fname}**")
			embed.add_field(name = f'**👑 Лидер семьи:**', value = f'<@{leader}>', inline=False)
			zam = []
			if fam.find_one({"name": amount, "guild": ctx.guild.id})["zam1"] == 1:
				zam.append(f'1. Не имеется\n')
			else:
				a = fam.find_one({"name": amount, "guild": ctx.guild.id})["zam1"]
				zam.append(f'1. <@{a}>\n')

			if fam.find_one({"name": amount, "guild": ctx.guild.id})["zam2"] == 1:
				zam.append(f'2. Не имеется\n')
			else:
				b = fam.find_one({"name": amount, "guild": ctx.guild.id})["zam2"]
				zam.append(f'2. <@{b}>\n')

			if fam.find_one({"name": amount, "guild": ctx.guild.id})["zam3"] == 1:
				zam.append(f'3. Не имеется\n')
			else:
				c = fam.find_one({"name": amount, "guild": ctx.guild.id})["zam3"]
				zam.append(f'3. <@{c}>\n')

			if fam.find_one({"name": amount, "guild": ctx.guild.id})["zam4"] == 1:
				zam.append(f'4. Не имеется\n')
			else:
				n = fam.find_one({"name": amount, "guild": ctx.guild.id})["zam4"]
				zam.append(f'4. <@{n}>\n')

			str_a = ''.join(zam)
			embed.add_field(name = "**🔱 Заместители:**", value = f"**{str_a}**", inline=False)

			var = []
			if fam.find_one({"name": amount, "guild": ctx.guild.id})["verf"] == 1:
				var.append(f'Имеется')
			else:
				var.append('Не имеется')

			str_b = ''.join(var)
			embed.add_field(name = "**✔ Галочка семьи**", value = f"**{str_b}**", inline = False)
			embed.add_field(name = "**🔶 Семейная роль:**", value = f"<@&{role1}>", inline=False)
			embed.add_field(name = "**🔷 Общее количество участников семьи:**", value = f"{len(role.members)}", inline=False)
			embed.add_field(name = "**🔺 Последний участник которому было отправлено приглашение:**", value = f"<@{member}>", inline=False)
			embed.add_field(name = "**🏆 Репутация семьи:**", value = f"{rep}", inline=False)
			embed.set_footer(text = f'Команды семьи: !famhelp | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
			await ctx.send(embed = embed)
		else:
			return await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(description = "Я не смог найти семью с таким названием.", colour = 0xFB9E14), delete_after = 20.0)

	@commands.command(aliases = ['разжаловать', 'rfz'])
	async def removefamzam(self, ctx, member: discord.Member = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		if fam.find_one({"leaderID": ctx.author.id, "guild": ctx.guild.id}):
			if member is None:
				await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #59**\'Возможные причины её возникновения:\n`•` Вы не указали пользователя, к которому должна применяться команда.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)
				return
			a = fam.find_one({"leaderID": ctx.author.id, "guild": ctx.guild.id})["roleID"]
			rolepr = discord.utils.get(ctx.guild.roles, id = a)
			if member.id == ctx.author.id:
				print('1')
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n>", description = f'Причины возникновения:\n`•` Вы указали пользователем самого себя.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

			if not rolepr in member.roles:
				print('2')
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n>", description = f'Причины возникновения:\n`•` Вы указали пользователем самого себя.\n`•` Выбранный пользователь не является участников Вашей семьи.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

			if not member.id in fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["id"]:
				print('3')
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n>", description = f'Причины возникновения:\n`•` Вы указали пользователем самого себя.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

			if fam.count_documents({"guild": ctx.guild.id, "leaderID": ctx.author.id}) == 0:
				return await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #402**\'Возможные причины её возникновения:\n**- Вы не вялетесь лидером семьи**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

			if not member.id in [i for i in fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["id"]]:
				return await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n>", description = f'Причины возникновения:\n- Пользователь не является заместителем семьи**\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

			mas = fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["id"]
			try: 
				mas.remove(member.id)
				mas.append(1)
			except: pass
			if fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam1"] == member.id: p = "zam1"
			elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam2"] == member.id: p = "zam2"
			elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam3"] == member.id: p = "zam3"
			elif fam.find_one({"guild": ctx.guild.id, "leaderID": ctx.author.id})["zam4"] == member.id: p = "zam4"

			fam.update_one({"guild": ctx.guild.id, "leaderID": ctx.author.id}, {"$set": {p: 1, "id": mas}})
			return await ctx.send( f'**`[ACCEPT]` {ctx.author.mention}`Вы успешно сняли права заместителя семьи с пользователя` {member.mention}**')
			
	@commands.command(aliases = ['назначить', 'afz'])
	async def addfamzam(self, ctx, member: discord.Member = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		if fam.find_one({"leaderID": ctx.author.id, "guild": ctx.guild.id}):
			if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id}):
				if fam.count_documents({"guild": ctx.guild.id, "leaderID": ctx.author.id}) == 0:
					print('1')
					return await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #402**\n- Причины возникновения:\n**- Вы не вялетесь лидером семьи**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

				if member == None:
					await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #217**\n- Причины возникновения:\n`•` Вы не указали пользователя, к которому должна применяться команда.\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)
					return
				if member == ctx.author:
					await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #217**\n- Причины возникновения:\n**- Вы не указали пользователем себя**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)
					return
				elif fam.find_one({"id": member.id, "guild": ctx.guild.id}):
					await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #88**\n- Причины возникновения:\n**- Вы указали пользователя который является лидером другой семьи**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)
				else:
					a = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["name"]
					m = await ctx.send(f"**`Вы действительно хотите назначить` {member.mention} `заместителем своей семьи? (+/-)`**")
					def check(m):
						return m.channel == ctx.channel and m.author == ctx.author
					try:
						msg = await self.bot.wait_for('message', check = check, timeout= 120.0)
					except TimeoutError:
						await ctx.message.delete()
						return await m.delete()
					else:
						if msg.content == "+":
							await msg.delete()
							if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam1"] == 1:
								await m.edit(content = f'**`[ACCEPT]` {ctx.author.mention}`Вы успешно назначили` {member.mention} `заместителем своей семьи!`**')
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"zam1": member.id}})
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"id": [ctx.author.id, member.id, 1]}})
								role = fam.find_one({"id": ctx.author.id})["roleID"]
								try:
									await member.add_roles(discord.utils.get(ctx.guild.roles, id = role.id))
								except:
									pass
								try:
									return await member.send(f"**Привет {member.display_name} тебя назначили заместителем семьи {a}:\n`Тебе доступны комманды:`\n> /faminvite @пользователь#1234 `- Пригласить в семью человека`\n> /fammenu `- Управление семьей`**")
								except:
									pass
							if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam2"] == 1:
								await m.edit(content = f'**`[ACCEPT]` {ctx.author.mention}`Вы успешно назначили` {member.mention} `заместителем своей семьи!`**')
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"zam2": member.id}})
								za = fam.find_one({"id": ctx.author.id})["zam1"]
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"id": [ctx.author.id, za, member.id]}})
								role = fam.find_one({"id": ctx.author.id})["roleID"]
								try:
									await member.add_roles(discord.utils.get(ctx.guild.roles, id = role.id))
								except:
									pass
								try:
									return await member.send(f"**Привет {member.display_name} тебя назначили заместителем семьи {a}:\n`Тебе доступны комманды:`\n> /faminvite @пользователь#1234 `- Пригласить в семью человека`\n> /fammenu `- Управление семьей`**")
								except:
									pass
							if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam3"] == 1:
								await m.edit(content = f'**`[ACCEPT]` {ctx.author.mention}`Вы успешно назначили` {member.mention} `заместителем своей семьи!`**')
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"zam3": member.id}})
								z = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam1"]
								za = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam2"]
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"id": [ctx.author.id, z, za, member.id, 1]}})
								role = fam.find_one({"id": ctx.author.id})["roleID"]
								try:
									await member.add_roles(discord.utils.get(ctx.guild.roles, id = role.id))
								except:
									pass
								try:
									return await member.send(f"**Привет {member.display_name} тебя назначили заместителем семьи {a}:\n`Тебе доступны комманды:`\n> /faminvite @пользователь#1234 `- Пригласить в семью человека`\n> /fammenu `- Управление семьей`**")
								except:
									pass
							if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam4"] == 1:
								await m.edit(content = f'**`[ACCEPT]` {ctx.author.mention}`Вы успешно назначили` {member.mention} `заместителем своей семьи!`**')
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"zam4": member.id}})
								z = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam1"]
								za = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["zam2"]
								role = fam.find_one({"id": ctx.author.id})["roleID"]
								try:
									await member.add_roles(discord.utils.get(ctx.guild.roles, id = role.id))
								except:
									pass
								fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"id": [ctx.author.id, z, za, za, member.id]}})
								try:
									return await member.send(f"**Привет {member.display_name} тебя назначили заместителем семьи {a}:\n`Тебе доступны комманды:`\n> /faminvite @пользователь#1234 `- Пригласить в семью человека`\n> /fammenu `- Управление семьей`**")
								except:
									pass
							else:
								await ctx.send(embed = discord.Embed(description = "**Произошла ошибка #418**\n- Причины возникновения:\n**- У вас уже есть 4  заместителя**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)
						else:
							await msg.delete()
							await m.edit(content = f'**`[Refused]` `Вы отклонили назначение заместителя`**', delete_after = 10)							
			else:
				await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n-", description = f'Причины возникновения:\n**- У вас не достаточно прав**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)
		else:
			await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n>", description = f"* Причины возникновения:**\n**- У вас не достаточно прав**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)

	@commands.command(aliases = ['fmenu'])
	async def fammenu(self, ctx):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		await ctx.message.delete()
		if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id}):
			embed = discord.Embed(description = f"**Привет, {ctx.author.mention}**, ты попал в меню управления семьёй!\n\nВот список доступных для вас действий:\n\n> 🔋 - `Изменить название семьи, внимание снимется 30 репутации.`\n> 🔖 - `Изменить роль семьи, внимание снимется 30 репутации.`\n> 💘 - `Получить галочку для семьи, внимание снимется 250 репутации.`\n\n> 📛 - **Закрыть**")
			message = await ctx.send(embed = embed)
			await message.add_reaction('🔋')
			await message.add_reaction('🔖')
			await message.add_reaction('💘')
			await message.add_reaction('📛')
			try:
				react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['🔋', '🔖', '💘', '📛'])
			except Exception:
				ctx.command.reset_cooldown(ctx)
				return await message.delete()
			else:
				await message.delete()
				if str(react.emoji) == '🔋':
					if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"] < 30:
						await ctx.send(embed = discord.Embed(title = '\⛩️ **__Ошибка выполнения:__**', description = 'У Вас недостаточно очков семейной репутации для совершения данного действия.\n`Необходимо:` 30'), delete_after = 7)
					else:
						ctx.command.reset_cooldown(ctx)
						m = await ctx.send("**`Напишите в чат название котрое хотите установить семье:`**")
						def check(m):
							return m.channel == ctx.channel and m.author == ctx.author
						try:
							msg = await self.bot.wait_for('message', check = check, timeout= 120.0)
						except TimeoutError:
							await ctx.message.delete()
							return await m.delete()
						else:
							await msg.delete()
							await m.edit(content = f'`[UPDATE]` `Название семьи было изменено!`\n1.`Новое название:` {msg.content}')
							fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"name": msg.content}})
							mem = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"]
							fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"mem": mem - 30}})
							return
				elif str(react.emoji) == '🔖':
					ctx.command.reset_cooldown(ctx)
					if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"] < 30:
						await ctx.send(embed = discord.Embed(title = '\⛩️ **__Ошибка выполнения:__**', description = 'У Вас недостаточно очков семейной репутации для совершения данного действия.\n`Необходимо:` 30'), delete_after = 7)
					else:
						m = await ctx.send("**`Напишите в чат название котрое хотите установить роли семье:`**")
						def check(m):
							return m.channel == ctx.channel and m.author == ctx.author
						try:
							msg = await self.bot.wait_for('message', check = check, timeout= 120.0)
						except TimeoutError:
							await ctx.message.delete()
							return await m.delete()
						else:
							await msg.delete()
							await m.edit(content = f'`[UPDATE]` `Название роли семьи было изменено!`\n1.`Новое название:` {msg.content}')
							role = discord.utils.get(ctx.guild.roles, id = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["roleID"])
							await role.edit(name = msg.content)
							mem = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"]
							fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"mem": mem - 30}})
							return

				elif str(react.emoji) == '💘':
					ctx.command.reset_cooldown(ctx)
					if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"] < 250:
						await ctx.send(embed = discord.Embed(title = '\⛩️ **__Ошибка выполнения:__**', description = 'У Вас недостаточно очков семейной репутации для совершения данного действия.\n`Необходимо:` 250'), delete_after = 7)
						return
					if fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["verf"] == 1:
						await ctx.send(embed = discord.Embed(description = f"{ctx.author.mention}** ошибка, у вас уже куплена галочка**"), delete_after = 15.0)
						return 
					else:
						embed = discord.Embed(title = "Галочка семьи", description = f"{ctx.author.mention}**, вы успешно преобрели галочку для вашей семьи!**")
						await ctx.send(embed = embed)
						fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"verf": 1}})
						a = fam.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["mem"]
						fam.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"mem": a - 250}})
						return
				elif str(react.emoji) == '📛':
					ctx.command.reset_cooldown(ctx)
					return
				else:
					return
		else:
			await ctx.send(embed = discord.Embed(title = "\⛩️ **__Произошла ошибка__**\n-", description = f'Причины возникновения:\n**- У вас не достаточно прав**\n\n`[Ps]:` Если вы не нашли в списке свою ошибку, обратитель к разработчику через [[В]Контакте](https://vk.com/dollarbabys)'), delete_after = 20.0)				

  @commands.command(aliases = ["семьи", "flist"])
	async def famlist(self, ctx):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		await ctx.message.delete()
		mas = [ ]
		index = 0
		for i in fam.find({"guild": ctx.guild.id}):
			index += 1
			mas.append(f'**`{index}.` Название:** {i["name"]}\n> `Лидер:` <@!{i["leaderID"]}>\n> `Семейная роль:` <@&{i["roleID"]}>\n> `Репутация:` {i["mem"]}\n')
		a = ''.join(mas)
		if len(a) == 0:
			return await ctx.channel.send(embed = discord.Embed(description = f'В данный момент, нет зарегистрированных семей.', colour = 0xFB9E14))
		else:
			return await ctx.channel.send(f'{ctx.author.mention}, список семей зарегистрированых на {ctx.guild.name}:', embed = discord.Embed(description = f'{a}', colour = 0xFB9E14))
        
	@commands.command(aliases = ["удалить", "fr"])
	@commands.has_permissions(administrator = True)
	async def removefam(self, ctx, *, amount: str = None):
		if not ctx.guild.id == 477547500232769536 and not ctx.guild.id == 577511138032484360: return
		await ctx.message.delete()
		if amount is None:
			return await ctx.send(embed = discord.Embed(description = f'❗ {ctx.author.name}, `вы не указали название семьи, которую хотите удалить!`\n\n**Пример использования команды:**\n> `{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}removefam(удалить|fr) [название]`\n-- Я предложу Вам удалить семью с максимально приближенным названием к вашему.', color = 0xFB0E14), delete_after = 7)
		mas = [i["name"] for i in fam.find({"guild": 477547500232769536})]
		b = 0
		for i in mas:
			if i.count(amount) > b:
				amount = i
				
		if fam.find_one({"name": amount, "guild": ctx.guild.id}):
			embed = discord.Embed(title = "Админ панель", description = f"**{ctx.author.mention}, была найдена семья по запросу {amount}.**\n> **Действия доступные вам:**\n> **💗 - Подтвердить удаление**\n> **💔 - Отменить удаление**")
			message = await ctx.send(embed = embed, delete_after = 30.0)
			await message.add_reaction("💗")
			await message.add_reaction("💔")
			try:
				react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['💗', '💔'])
			except Exception:
				ctx.command.reset_cooldown(ctx)
				return await message.delete()
			else:
				await message.delete()
				if str(react.emoji) == '💗':
					ctx.command.reset_cooldown(ctx)
					if fam.find_one({"name": amount, "guild": ctx.guild.id}):
						nam = fam.find_one({"name": amount, "guild": ctx.guild.id})
						try:
							own = discord.utils.get(ctx.guild.members, id = nam["leaderID"])
							owner = f'{own.mention}`({own})`'
						except:
							owner = 'Не найден'
						try:
							role = discord.utils.get(ctx.guild.roles, id = nam["roleID"])
							await discord.utils.get(ctx.guild.roles, id = nam["roleID"]).delete()
						except: pass
						await discord.utils.get(ctx.guild.channels, id = nam["channel"]).delete()
						embed = discord.Embed(title = "Удаление семьи", description = f"**{ctx.author.mention}, вы успешно удалили семью {amount}**\n**Вот ее параметры:**\n\n1. `Владелец семьи:` **{owner}**\n2. `Семейная роль:` **{role.name}**")
						embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
						await ctx.send(embed = embed)
						fam.delete_one({"name": amount})
					else:
						return

				if str(react.emoji) == '💔':
					ctx.command.reset_cooldown(ctx)
					if fam.find_one({"name": amount, "guild": ctx.guild.id}):
						embed = discord.Embed(title = "Удаление семьи", description = f"**{ctx.author.mention}, вы отменили свое действие")
						embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
						await ctx.send(embed = embed, delete_after = 10.0)
					else:
						return
		else:
			await ctx.send("**`[Err]` Я не нашел семью с таким названием!**", delete_after = 10.0)


def setup(bot):
	bot.add_cog(family(bot))
