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
bmafia = db["mafia"] 


# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

global force, cids, prov, chisla, chisla1, get_role, players, role, game, messageid, coold, delb
force, cids, prov, chisla, chisla1, get_role, players, role, game, messageid, coold, delb = [ ], [ ], 0, ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'], ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'], [ ], [ ], ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Ночная Бабочка'], 0, 0, 0, 0


def setembed(title = None, thumb = None, footer = None, *, text):
    if title is None:
        embed = discord.Embed(description = f'{text}', colour=0xFB9E14)
    else:
        embed = discord.Embed(title = title, description = f'{text}', colour=0xFB9E14)
    if not thumb is None:
        embed.set_thumbnail(url = thumb)
    if footer == None:
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    else:
        embed.set_footer(text = f'{footer} | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')

    return embed

class mafia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog TestMafia by dollar ム baby#3603 успешно запущен!')

    @commands.command()
    async def mhelp(self, ctx):
        message = await ctx.send(embed = setembed(title = 'Команды игры в мафию', thumb = ctx.guild.icon_url, footer = '❌ - Закрыть', text = f'**💬 | Выдача времени:**\n> **`Ознакомительная, За столом, Предсмертная речи` - 1 Минута**\n> **`Оправдательная речь` - 30 секунд**\n> **Речь за столом после 0 круга, должна быть не менее 20 секунд.** `За нарушение выдаётся фол`\n> **События происходят в городе**\n\n💬 Список команд\n> **`/msts` - Начать игру**\n> **1. `/убить <member/memberID>` - Убить игрока**\n> **2. `/фол <member/memberID>` - Выдать фол игроку**\n> **3. `/унфол <member/memberID>` - Снять фол игроку**\n> **4. `/night` - Устанавовить режим "Ночь"(выключение микрофонов и закрытие чата)**\n> **6. `/day` - Установить режим "День"(Включение микрофонов и открытие чата, если у игрока 3 фола, мут не снимает)**\n> **7. `/mstop` - Закончить мафию**\n> **8. `/выставить <member/memberID>` - Выставить игрока на голосование**\n> **9. `/ungolos <member/memberID>` - Снять игрока с голосования**\n> **10. `/голосование` - Запустить режим голосования в канале "Чат-Мафии"**\n> **11. `/golist` - Посмотреть список проголосовавших.**\n> **12. `/линк` - Сделать упоминание о мафии(Раз в 10 минут)**\n> **13. `/heal` - Вернуть пользователя в игру(Если был убит по ошибке)**\n> **14. `/swap_ved @Пользователь#1234` - Передать права ведущего пользователю**\n> **15. `/gamerole` - Запросить список игроков мафии с описанием их ролей**\n**[P.S]: `/act` - Если игра забагалась, пишите это и после `/mstop`**\n\n**Доступно только ведущим!**'))
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌'])
        except Exception:
            return await message.delete()
        else:
            if str(react.emoji) == '❌':
                return await message.delete()


    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.member)
    async def msts(self, ctx):

        if not ctx.guild.id == 477547500232769536:
            ctx.command.reset_cooldown(ctx)
            return

        global prov 
        global messageid

        await ctx.message.delete()

        if not discord.utils.get(ctx.guild.roles, id = 820012796523446352) in ctx.author.roles:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f'`[ERROR]` `Ошибка доступа!`', delete_after = 3)
            
        if prov == 1:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f'`[ERROR]` `Набор участников уже запущен!`', delete_after = 3)

        prov = 1
        mes1 = await ctx.send('`[INFO]` `Если вы желаете сделать оповещение, введите + в чат\nДля отмены напишите любое сообщение.`')
        def check(link):
            return link.author.id == ctx.author.id and link.channel.id == ctx.channel.id
        msg = await self.bot.wait_for('message', check=check)
        if msg.content == '+':
            await mes1.delete()
            await msg.delete()
            channel = discord.utils.get(ctx.guild.channels, id = 806214892012830770)
            embed = discord.Embed(title = 'Игра в мафию', description = f'**Всем привет :)\nХочу сообщить Вам хорошую новость!\nПрямо сейчас, в нашем Дискорде будет проходить Мафия\nЕсли Вы хотите поиграть с нами, ждём вас в канале {channel.mention}\n\nДля игры требуется:\n> `Рабочий микрофон`\n> `Желание поиграть`**', colour = 0xFB9E14)
            await ctx.send(f'{ctx.guild.default_role}', embed = embed, delete_after = 600)
        else:
            await mes1.delete()
            await msg.delete()
        embed = discord.Embed(title = 'Игра в мафию', description = f'**Ведущий: {ctx.author.mention}**\nВ данный момент пользователей нет.\nНажмите ✔️ что бы принят участие!', colour = 0xFB9E14, timestamp = ctx.message.created_at)
        embed.set_footer(text = f'❌ - Отменить | ▶️ - Запустить | ❔ - Проверить')
        mes = await ctx.send(embed = embed)
        players.append(ctx.author.id)
        bmafia.insert_one({"guild": ctx.guild.id, "ved": ctx.author.id, "id": ctx.author.id, "name": ctx.author.display_name, "role": 0, "mesid": mes.id, "meschan": ctx.channel.id, "del": 1, "night": 0, "nicks": 0, "leader": 1})
        await mes.add_reaction('✔️')
        await mes.add_reaction('❌')
        await mes.add_reaction('▶️')
        await mes.add_reaction('❔')
        cids.append(ctx.channel.id)
        messageid = mes.id

    @commands.command(aliases = ['оповещение', 'линк'])
    @commands.cooldown(1, 600, commands.BucketType.member)
    async def link(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            ctx.command.reset_cooldown(ctx)
            return

        await ctx.message.delete()

        if not prov == 1:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f'`[ERROR]` `Набор участников не запущен!`', delete_after = 3)
        

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f'`[ERROR]` `Вы не ведущий!`', delete_after = 3)

        else:
            channel = discord.utils.get(ctx.guild.channels, id = 806214892012830770)
            embed = discord.Embed(title = 'Игра в мафию', description = f'**Всем привет :)\nХочу сообщить Вам хорошую новость!\nПрямо сейчас, в нашем Дискорде будет проходить Мафия\nЕсли Вы хотите поиграть с нами, ждём вас в канале {channel.mention}\n\nДля игры требуется:\n> `Рабочий микрофон`\n> `Желание поиграть`**', colour = 0xFB9E14)
            await ctx.send(f'{ctx.guild.default_role}', embed = embed, delete_after = 600)
    
    @commands.Cog.listener()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def on_raw_reaction_add(self, payload):
        global players
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return

        if not guild.id == 477547500232769536:
            return

        global force
        global prov
        global chisla
        global chisla1
        global get_role
        global role
        global game
        global coold
        global messageid
        global delb

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            channel = self.bot.get_channel(payload.channel_id)
            if channel.id == 505009452571820032 or not channel.id == 885503856556011570:
                return
            message = await channel.fetch_message(payload.message_id)
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            emoji = str(payload.emoji)
            vchannel = self.bot.get_channel(806214892012830770)

            if channel.id == bmafia.find_one({"guild": guild.id})["meschan"] and message.id == bmafia.find_one({"guild": guild.id})["mesid"]:
                if emoji == '✔️':

                    if memb.id in players:
                        return

                    vchannel = self.bot.get_channel(806214892012830770)

                    if len(force) == 10:
                        return await channel.send('`[ERROR]` `В данный момент кол-во участников является максимальным.`', delete_after = 2)

                    if not memb in vchannel.members:
                        return await channel.send(f'`[ERROR]` `Вам нужно находиться в голосовом канале` {vchannel.mention}', delete_after = 3)

                    if coold == 1:
                        delb = memb.id
                        return await channel.send(f'`[ERR]` {memb.mention}, `подождите пока будет записан другой участник.`', delete_after = 2)

                    if memb.id == bmafia.find_one({"leader": 1})["ved"]:
                        return 
                    
                    coold = 1

                    force.append(f'\n<@!{memb.id}>')
                    str_a = ''.join(force)
                    if len(force) == 10:
                        source = 'Нет'
                    else:
                        source = f'{10 - len(force)}\nНажмите ✔️ что бы принять участие!'
                    embed = discord.Embed(title = 'Игра в мафию', description = f'**Ведущий: <@!{bmafia.find_one({"leader": 1})["ved"]}>**\n**Пользователи:** {str_a}\n**Свободых мест: {source}**', colour = 0xFB9E14, timestamp = message.created_at)
                    embed.set_footer(text = f'❌ - Отменить | ▶️ - Запустить | ❔ - Проверить')
                    await message.edit(embed = embed)
                    players.append(memb.id)
                    coold = 0

                if emoji == '❌':
                    if not memb.id == bmafia.find_one({"leader": 1})["ved"]:
                        return
                    
                    await message.delete()

                    global game
                    global role
                    global get_role
                    global prov
                    global chisla
                    global chisla1

                    guild = self.bot.get_guild(payload.guild_id)

                    prov = 0
                    game = 0
                    chisla1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
                    chisla = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
                    get_role = [ ]
                    role = ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Ночная Бабочка']
                    rol = discord.utils.get(guild.roles, id = 914455571741167646)
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel = False, read_messages=False, read_message_history = False),
                        rol: discord.PermissionOverwrite(view_channel = True, read_messages=True, send_messages = True, read_message_history = True)
                        }
                    chan = self.bot.get_channel(885503856556011570)
                    for i in bmafia.find({"guild": guild.id}):
                        member = discord.utils.get(guild.members, id = i["id"])
                        try: await member.edit(nick = i["name"])
                        except: pass
                    await chan.edit(overwrites = overwrites)
                    await chan.purge(limit = 1000)

                    for i in bmafia.find({"guild": guild.id}):
                        bmafia.delete_one({"id": i["id"]})

                    force = [ ]
                    prov = 0
                    game = 0

                    self.bot.reload_extension(f'cogs.mafia')
                    return await channel.send('`[TRY]` `Игра была остановлена её организатором.`', delete_after = 10)
                if emoji == '▶️':
                    if not memb.id == bmafia.find_one({"leader": 1})["ved"]:
                        return

                    if not memb in vchannel.members:
                        return await channel.send(f'`[ERROR]` `Вам нужно находиться в голосовом канале` {vchannel.mention}', delete_after = 5)

                    if game == 1:
                        await self.bot.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                        return await channel.send('`[ERROR]` `Игра уже запущена!`', delete_after = 2)
                    
                    if not len(force) < 10:
                        await self.bot.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                        return await channel.send('`[ERROR]` `В данный момент не достаточно участников для начала игры!`', delete_after = 3)

                    await message.delete()

                    prov = 0
                    game = 1
                    guild = self.bot.get_guild(payload.guild_id)
                    f = 0
                    mafadd = self.bot.get_channel(806215783121289297)
                    igr = discord.utils.get(guild.roles, id = 914455571741167646)
                    dm = 0
                    mf = 0
                    force = [ ]
                    messageid = 0
                    role = ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Ночная Бабочка']

                    for i in players:
                        member = discord.utils.get(guild.members, id = i)
                        if member.id == bmafia.find_one({"leader": 1})["ved"]:
                            try: await member.edit(nick = '[MAFIA]: Ведущий')
                            except: pass
                            vedid = member.id
                            continue
                        else:
                            guild = self.bot.get_guild(payload.guild_id)

                            name = member.display_name
                            await member.add_roles(igr)
                            bmafia.insert_one({"guild": guild.id, "ved": 0, "id": member.id, "name": member.display_name, "role": 0, "del": 1, "night": 0, "nicks": 0, "golos": 777, "active": 1, "fols": 0, "num": min(chisla)})
                            try: await member.edit(nick = f'{min(chisla)}')
                            except: pass
                            chisla.remove(min(chisla))
                            a = random.randint(0, len(role) - 1)
                            embed = discord.Embed(description = f'**Привет {member.mention}! Ты учавствуешь в мафии на сервере {guild.name} :)**', colour = 0xFB9E14)
                            ath = re.split(r'\W+', str(role[a]))
                            if role[a] == 'Дон мафии':
                                chan = self.bot.get_channel(806215783121289297)
                                await chan.set_permissions(member, read_messages = True, view_channel = True, send_messages = True, read_message_history = True)
                                embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Дон Мафии**\n> `Канал тёмной стороны:` {chan.mention}.', inline = False)
                                get_role.append(f'> 🧛‍♂ `Дон Мафии -` {member.display_name} | `Nick:` **{name} | `ID:` {member.id}**\n')
                                role.remove('Дон мафии')
                                await chan.send(embed = discord.Embed(description = f'Привет! Данный чат создан для тёмной стороны города! Доступ в него имеют только красные отрицательные роли: Мафия, Дон Мафии.\n\nОтправлять сообщения о убийстве и проверке необходимо Дону Мафии\n**Форма отправки сообщения от {member.mention}:**\n{memb.mention}, килл(номер), чек(номер)\n\n❗ ❗ ВАЖНО ❗ ❗\n> `Сообщение отправленное по другой форме будет отклонено`\n> `Сообщение без упоминание ведущего будет отклонено`\n> `Сообщение нет от Дона Мафии(Если жив) будет отклонено.`\n❗ ❗ ВАЖНО ❗ ❗'))
                                dm = member.id
                            elif role[a] == 'Мафия':
                                chan = self.bot.get_channel(806215783121289297)
                                await chan.set_permissions(member, read_messages = True, view_channel = True, send_messages = True, read_message_history = True)
                                embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Мафия**\n> `Канал тёмной:` {chan.mention}.', inline = False)
                                get_role.append(f'> 🤵 `Мафия -` {member.display_name} | `Nick:` **{name} | `ID:` {member.id}**\n')
                                mf = member.id
                                role.remove('Мафия')
                            elif role[a] == 'Шериф':
                                embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Шериф**', inline = False)
                                embed.add_field(name = '`Форма:`', value = f'**Вы должны писать ведущему {memb.mention}({memb.display_name}) следующее сообщение:** `Проверяю игрока "Номер"`')
                                get_role.append(f'> 🕵 `Шериф -` {member.display_name} | `Nick:` **{name} | `ID:` {member.id}**\n')
                                role.remove('Шериф')
                            elif role[a] == 'Врач':
                                embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Врач**', inline = False)
                                embed.add_field(name = '`Форма:`', value = f'**Вы должны писать ведущему {memb.mention}({memb.display_name}) следующее сообщение:** `Лечу игрока "Номер"`')
                                get_role.append(f'> 👨‍⚕ `Врач -` {member.display_name} | `Nick:` **{name} | `ID:` {member.id}**\n')
                                role.remove('Врач')
                            elif role[a] == 'Ночная Бабочка':
                                embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Ночная Бабочка**', inline = False)
                                embed.add_field(name = '`Форма:`', value = f'**Вы должны писать ведущему {memb.mention}({memb.display_name}) следующее сообщение:** `Провожу ночь с игроком "Номер"`')
                                get_role.append(f'> 🧚🏻‍♂️ `Ночная Бабочка -` {member.display_name} | `Nick:` **{name} | `ID:` {member.id}**\n')
                                role.remove('Ночная Бабочка')
                            elif ath[0] == 'Мирный':
                                f += 1
                                embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Мирный житель**', inline = False)
                                get_role.append(f'> 👨‍💻 `Мирный житель -` {member.display_name} | `Nick:` **{name} | `ID:` {member.id}**\n')
                                role.remove(f'Мирный житель {f}')
                            try:
                                await member.send(embed = embed, delete_after = 600)
                            except discord.Forbidden: 
                                guild = self.bot.get_guild(payload.guild_id)
                                chisla1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
                                chisla = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
                                get_role = [ ]
                                role = ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Ночная Бабочка']
                                rol = discord.utils.get(guild.roles, id = 914455571741167646)
                                overwrites = {
                                    guild.default_role: discord.PermissionOverwrite(view_channel = False, read_messages=False, read_message_history = False),
                                    rol: discord.PermissionOverwrite(view_channel = True, read_messages=True, send_messages = True, read_message_history = True)
                                    }
                                chan = self.bot.get_channel(885503856556011570)
                                await chan.edit(overwrites = overwrites)
                                await chan.purge(limit = 1000)
                                chann2 = self.bot.get_channel(806215020333236244)
                                await chann2.purge(limit = 1000)
                                self.bot.reload_extension(f'cogs.mafia')
                                return await channel.send(f'`[System]` `Система дала отрицательный результат при проверке сообщения пользователя {member.display_name}`({member.mention})', delete_after = 10)
                        
                    if dm > 1:
                        bmafia.update_one({"id": dm}, {"$set": {"role": "Дон мафии"}})
                    if mf > 1:
                        bmafia.update_one({"id": mf}, {"$set": {"role": "Мафия"}})


                    embed = discord.Embed(description = f'**Привет мафиозники! Приветствую всех в игре под названием "Мафия"!**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                    embed.add_field(name = '🛡️ Правила игры', value = '**На всё лобби раздаётся 10 ролей, каждая из них должна выполнять определённые действия.**\n> `Главная цель белой стороны:` **Раскрыть всех тёмных личностей**.\n> `Главная цель тёмной стороны:` **Убить всех белых личностей**', inline = False)
                    embed.add_field(name = '🚀 В данной игре запрещено', value = '> Перебивать ведущего\n> Разговаривать в ночное время.\n> Заключать содружетсво между враждующими сторонами\n> Бездействовать\n> Оскорблять кого-либо', inline = False)
                    embed.add_field(name = '🌟 `Роли игроков`', value = '> Мафия\n> Дон мафии\n> Врач\n> Шериф\n> 6 Мирных жителей\n\n', inline = False)
                    embed.add_field(name = '💬 `Что делает Мафия?`', value = '**Убивает людей по ночам. Старается убирать "Красные роли", то есть шерифа или врача, для того чтобы те не смогли рассекретить мафию или исцелить её жертв. Для убийства 1 человека, необходимо согласие самой Мафии и Дона мафии. После убийства, жертва выбывает из игры, если её не исцелит Врач. Победа мафии объявляется только в том случае, если из игры выбывают все игроки имеющие красные роли**', inline = False)
                    embed.add_field(name = '💬 `Что делает Шериф?`', value = '**Он является активной "Красной ролью". Задача шерифа- найти и рассекретить мафию и Дона Мафии. После действий шерифа - человек на которого были возложены обвинения выбывает из игры.**', inline = False)
                    embed.add_field(name = '💬 `Что делает Врач?`', value = '**У человека с этой ролью есть возможность исцелять 1 любого человека на его выбор включая себя, каждую ночь. При этом, ему запрещается лечить себя 2 раза за игру. Если он исцеляет игрока, которого выбрала сторона мафии - игрок остаётся в игре.**', inline = False)
                    embed.add_field(name = '💬 `Что делают Мирные жители?`', value = '**Задача этой роли, путём дневного обсуждения вычислить мафию. Человек с этой ролью имеет право последнего слово и может озвучить свои подозрения в сторону любого игрока.**', inline = False)
                    embed.add_field(name = '💬 `Выдача времени`', value = f'> **Ознакомительная, За столом, Предсмертная речи - 1 Минута\n> Оправдательная речь - 30 секунд\n> Речь за столом после 0 круга, должна быть не менее 20 секунд. `За нарушение выдаётся фол`\n> События происходят в городе**')
                    embed.add_field(name = '🎮 `На этом мы подошли к концу`', value = f'**Наша команда желает Вам удачи в самой игре и приятного времяпровождения в Discord Канале {guild.name} ❤️**')
                    embed.set_author(name = 'Мафия Информатор', url = 'https://vk.com/dollarbabys', icon_url = 'https://sun9-36.userapi.com/c854428/v854428073/228488/tvUKvnDpcdk.jpg')
                    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                    embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                    mesch = await mafadd.send(embed = embed)
                    players = [ ]
                    bmafia.update_one({"id": vedid}, {"$set": {"mesid": mesch.id, "meschan": mafadd.id}})

                    str_a = ''.join(get_role)
                    embed = discord.Embed(description = f'**Список игроков:**\n{str_a}\n**Можно начинать!**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                    embed.set_author(name = 'Информация для ведущего', url = 'https://vk.com/dollarbabys', icon_url = 'https://sun9-36.userapi.com/c854428/v854428073/228488/tvUKvnDpcdk.jpg')
                    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                    embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                    
                    await discord.utils.get(guild.members, id = vedid).send(embed = embed)
                if emoji == '❔':

                    if not memb.id == bmafia.find_one({"leader": 1})["ved"]:
                        return

                    await channel.send('`[System]` `Начинаю проверку пользователей на доступ к отправке сообщений. Если бот прекратил отправлять сообщения - пользователь заблокировал доступ к отправке сообщений.`', delete_after = 10)
                    guild = self.bot.get_guild(payload.guild_id)
                    for i in bmafia.find({"guild": guild.id}):
                        member = discord.utils.get(guild.members, id = i["id"])
                        try:
                            await member.send('`[System]` `Системная проверка...`', delete_after = 1)
                        except discord.Forbidden: 
                            await self.bot.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                            return await channel.send(f'`[System]` `Система дала отрицательный результат при проверке пользователя {member.display_name}.`', delete_after = 5)

                        await channel.send(f'`[System]` `Пользователь {member.display_name} проверен.`', delete_after = 1)

                    return await channel.send('`[System]` `Проверка успешно закончена. У всех участников мафии открыт доступ в личные сообщения.`', delete_after = 5)

    @commands.command()
    async def act(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        if not discord.utils.get(ctx.guild.roles, id = 820012796523446352) in ctx.author.roles:
            return
            
        await ctx.message.delete()
        global game

        game = 1
        return await ctx.send('+', delete_after = 1)

    @commands.command()
    async def mstop(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return
        global game
        global role
        global get_role
        global prov
        global chisla
        global chisla1
        global force

        if game == 0:
           return await ctx.send('`[ERROR]` `Игра не запущена.`', delete_after = 5)

        await ctx.message.delete()
  
        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        prov = 0
        game = 0
        force = [ ]
        chisla1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        chisla = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        get_role = [ ]
        role = ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Ночная Бабочка']
        rol = discord.utils.get(ctx.guild.roles, id = 914455571741167646)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False, read_messages=False, read_message_history = False),
            rol: discord.PermissionOverwrite(view_channel = True, read_messages=True, send_messages = True, read_message_history = True)
            }

        chan = self.bot.get_channel(885503856556011570)
        for i in bmafia.find({"guild": ctx.guild.id}):
            member = discord.utils.get(ctx.guild.members, id = i["id"])
            try:
              await member.edit(nick = i["name"])
            except:
              pass
        await chan.edit(overwrites = overwrites)
        await chan.purge(limit = 1000)
        chann2 = self.bot.get_channel(806215020333236244)
        await chann2.purge(limit = 1000)
        vchannel1 = self.bot.get_channel(806214892012830770)
        uch = discord.utils.get(ctx.guild.roles, id = 914455571741167646)
        for i in vchannel1.members:
            if uch in i.roles:
                await i.remove_roles(uch)

            await i.edit(mute = False)

        for i in bmafia.find({"guild": ctx.guild.id}):
            bmafia.delete_one({"id": i["id"]})

        self.bot.reload_extension(f'cogs.mafia')
        await ctx.send(f'`[ACCEPT]:` {ctx.author.mention}, `мафия была успешно окончена!`')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global players
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 477547500232769536:
            return

        global force
        global delb

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass

        else:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            emoji = str(payload.emoji)
            
            if user.bot:
                return

            if not f'\n<@!{memb.id}>' in force:
                return

            for i in bmafia.find({"leader": 1}):
                if channel.id == i["meschan"]:

                    if emoji == '✔️':
                        
                        if i["ved"] == memb.id:
                            return

                        if delb == memb.id:
                            return delb == 0

                        players.remove(memb.id)
                        force.remove(f'\n<@!{memb.id}>')
                        str_a = ''.join(force)
                        if len(force) == 0:
                            embed = discord.Embed(title = 'Игра в мафию', description = f'**Ведущий: <@!{i["ved"]}>**\n**Пользователей нет.\nНажмите ✔️ что бы принять участие!**', colour = 0xFB9E14, timestamp = message.created_at)
                        else:
                            if len(force) == 10:
                                source = 'Нет'
                            else:
                                source = f'{10 - len(force)}\nНажмите ✔️ что бы принять участие!'
                            embed = discord.Embed(title = 'Игра в мафию', description = f'**Ведущий: <@!{i["ved"]}>**\n**Пользователи:** {str_a}\n**Свободых мест: {source}**', colour = 0xFB9E14, timestamp = message.created_at)
                            embed.set_footer(text = f'❌ - Отменить | ▶️ - Запустить | ❔ - Проверить')
                        await message.edit(embed = embed) 

    @commands.command(aliases = ['фол'])
    async def fol(self, ctx, member: discord.Member = None):

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if member == None:
            return await ctx.send('`[ERROR]` `Укажите пользователя!`', delete_after = 5)

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if bmafia.count_documents({"id": member.id}) == 0:
            return await ctx.send('`[ERROR]` `Вы не можете выдать фол пользователю который не учавствует в игре.`', delete_after = 5) 
        
        if member.id == bmafia.find_one({"leader": 1})["ved"]:
            return
            
        if not bmafia.find_one({"id": member.id})["active"] == 0:
            if bmafia.find_one({"id": member.id})["fols"] == 3:
                bmafia.update_one({"id": member.id}, {"$set": {"active": 0}})
                embed = discord.Embed(description = f'**Пользователь {member.mention} был выгнан из игры.**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = f'Фолов: 4/4')
                text = f'`[System]: Игрок {member.display_name}({bmafia.find_one({"leader": 1})["name"]}) был получил 4 фола и был исключён из игры.`'
                fol = bmafia.find_one({"id": member.id})["fols"] + 1
                uname = f'{bmafia.find_one({"id": member.id})["nicks"]}[Фолов: 3/4]'
                bmafia.update_one({"id": member.id}, {"$set": {"active": 0, "nicks": uname, "fols": fol}})
                await member.edit(nick = bmafia.find_one({"id": member.id})["name"])
                for z in self.bot.get_channel(806214892012830770).members:
                    await z.send(text)
                vhannel = self.bot.get_channel(806214892012830770)
                uch = discord.utils.get(ctx.guild.roles, id = 914455571741167646)
                if uch in member.roles:
                    await member.remove_roles(uch)

                if member in vhannel.members:
                    await member.edit(mute = False)

                return await ctx.send(embed = embed)

            if bmafia.find_one({"id": member.id})["fols"] == 0:
                lf = 0
                mas = [ ]
                for b in list(member.display_name):
                    mas.append(b)
                    lf += 1
                    if lf == 2:
                        break

                strr_a = ''.join(mas)
                bmafia.update_one({"id": member.id}, {"$set": {"nicks": strr_a}})

            fol = bmafia.find_one({"id": member.id})["fols"] + 1

            bmafia.update_one({"id": member.id}, {"$set": {"fols": fol}})
            if fol == 1:
                await member.edit(nick = f'{strr_a}[Фолов: {fol}/4]')
            else:
                await member.edit(nick = f'{bmafia.find_one({"id": member.id})["nicks"]}[Фолов: {fol}/4]')
            if fol == 3:
                embed = discord.Embed(description = f'**Пользователь {member.mention} пропускает следующую речь.\nПри получении ещё одного фола, он будет исключён из игры.**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = f'Фолов: {fol}/4')
                vhannel = self.bot.get_channel(806214892012830770)
                if member in vhannel.members:
                    await member.edit(mute = True)
                return await ctx.send(embed = embed)
            embed = discord.Embed(description = f'**Пользователь {member.mention} получает фол!**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
            embed.set_footer(text = f'Фолов: {fol}/4')
            return await ctx.send(embed = embed)
        
    @commands.command(aliases = ['унфол'])
    async def unfol(self, ctx, member: discord.Member = None):

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if member == None:
            return await ctx.send('`[ERROR]` `Укажите пользователя!`', delete_after = 5)

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if bmafia.count_documents({"id": member.id}) == 0:
            return await ctx.send('`[ERROR]` `Вы не можете применить это действие пользователю который не учавствует в игре.`', delete_after = 5) 

        if member.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if not bmafia.find_one({"id": member.id})["active"] == 0:
            if bmafia.find_one({"id": member.id})["fols"] == 0:
                return await ctx.send('`[ERROR]` `Пользователь не имеет фолов.`', delete_after = 5)

            fol = bmafia.find_one({"id": member.id})["fols"] - 1
            bmafia.update_one({"id": member.id}, {"$set": {"fols": fol}})
            if fol == 2:
                await member.edit(mute = False)
            await member.edit(nick = f'{bmafia.find_one({"id": member.id})["nicks"]}[Фолов: {fol}/4]')
            embed = discord.Embed(description = f'**Пользователю {member.mention} сняли 1 фол!**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
            embed.set_footer(text = f'Фолов: {fol}/4')
            return await ctx.send(embed = embed)
    
    @commands.command(aliases = ['убить'])
    async def mafkill(self, ctx, member: discord.Member = None, arg = None):
        global get_role
        global game

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if not game == 1:
            return

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if bmafia.count_documents({"id": member.id}) == 0:
            return await ctx.send('`[ERROR]` `Вы не можете выдать убить пользователя который не учавствует в игре.`', delete_after = 5) 

        if member.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if not bmafia.find_one({"id": member.id})["active"] == 0:
            try:
                uch = discord.utils.get(ctx.guild.roles, id = 914455571741167646)
                if uch in member.roles:
                    await member.remove_roles(uch)

                if bmafia.find_one({"id": member.id})["role"] == 'Мафия' or bmafia.find_one({"id": member.id})["role"] == 'Дон мафии':
                    chan = self.bot.get_channel(885503856556011570)
                    await chan.set_permissions(member, read_messages = False, view_channel = False, send_messages = False, read_message_history = False)
                if bmafia.find_one({"id": member.id})["fols"] == 0:
                    uname = member.display_name
                else:
                    uname = f'0{bmafia.find_one({"id": member.id})["nicks"]}[Фолов: {bmafia.find_one({"id": member.id})["fols"]}/4]'
                bmafia.update_one({"id": member.id}, {"$set": {"active": 0, "nicks": uname}})
                mchannel = self.bot.get_channel(806215020333236244)
                embed = discord.Embed(description = f'**Пользователь {member.mention} покидает наш стол.**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = f'Спасибо за участие, {member}!')
                if not arg == None:
                    embed.add_field(name = '`Действие`', value = f'**Игрок был повешан на городском голосовании!**')
                    text = f'`[System]: Игрок {member.display_name}({bmafia.find_one({"id": member.id})["name"]}) покидает стол!`\n> `Был повешан на голосовании!`'
                else:
                    embed.add_field(name = '`Действие`', value = f'**Игрок был убит мафией!**')
                    text = f'`[System]: Игрок {member.display_name}({bmafia.find_one({"id": member.id})["name"]}) покидает стол!`\n> `Был убит мафией!`'

                await mchannel.send(embed = embed)

                for z in self.bot.get_channel(806214892012830770).members:
                    await z.send(text, delete_after = 15)
                await member.edit(nick = bmafia.find_one({"id": member.id})["name"])

            except:

                return await ctx.send('`[ERROR]` `Неизвестная ошибка`', delete_after = 3)

    @commands.command(aliases = ['heal'])
    async def вернуть(self, ctx, member: discord.Member = None):
        global get_role
        global game

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if not game == 1:
            return

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if bmafia.count_documents({"id": member.id}) == 0:
            return await ctx.send('`[ERROR]` `Нельзя применить для пользователя который не учавствует в игре.`', delete_after = 5) 

        if member.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if not bmafia.find_one({"id": member.id})["active"] == 0:
            return await ctx.send(f'`[ERROR]` {ctx.author.mention}, `данный игрок не умер.`', delete_after = 5)

        if not member in self.bot.get_channel(806214892012830770).members:
            return await ctx.send(f'`[ERROR]` {ctx.author.mention}, `возрождаемый игрок должен находиться в канале проведения мафии!`', delete_after = 5)

        if bmafia.find_one({"id": member.id})["role"] == 'Мафия' or bmafia.find_one({"id": member.id})["role"] == 'Дон мафии':
            chan = self.bot.get_channel885503856556011570)
            await chan.set_permissions(member, read_messages = True, view_channel = True, send_messages = True, read_message_history = True)
        
        mchannel = self.bot.get_channel(806215020333236244)
        await member.add_roles(discord.utils.get(ctx.guild.roles, id = 914455571741167646))

        embed = discord.Embed(description = f'**Пользователь {member.mention} возвращается в нашу игру**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        embed.set_footer(text = f'Приянтной игры, {member}!')
        if bmafia.find_one({"id": member.id})["fols"] == 4:  
            bmafia.update_one({"id": member.id}, {"$set": {"active": 1, "fols": 3}})
            await member.edit(nick = f'{bmafia.find_one({"id": member.id})["num"]}[Фолов 3/4]')
        else:
            sets = bmafia.find_one({"id": member.id})["fols"]
            await member.edit(nick = f'{bmafia.find_one({"id": member.id})["num"]}[Фолов {sets}/4]')
        embed.add_field(name = '`Информация:`', value = f'**Игрок {member.mention} был восстановлен ведущим\nНомер игрока: {bmafia.find_one({"id": member.id})["num"]}\nАккаунт: {bmafia.find_one({"id": member.id})["name"]}\nФолов: {sets}/4**')
        bmafia.update_one({"id": member.id}, {"$set": {"active": 1}})

        await mchannel.send(embed = embed)

    @commands.command(aliases = ['giveved'])
    async def swap_ved(self, ctx, member: discord.Member = None):
        global get_role
        global game

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if not game == 1:
            return

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if member.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        if not member in self.bot.get_channel(806214892012830770).members:
            return await ctx.send(f'`[ERROR]` {ctx.author.mention}, `данный пользователь должен находиться в канале проведения мафии!`', delete_after = 5)

        if bmafia.count_documents({"id": member.id}) == 1:
            return await ctx.send(f'`[ERROR]` {ctx.author.mention}, `пользователю являющемуся игроком действующей мафии нельзя передать руководство.`', delete_after = 5)

        await ctx.author.edit(nick = bmafia.find_one({"id": ctx.author.id})["name"])  
        bmafia.delete_one({"id": ctx.author.id})
        bmafia.insert_one({"guild": ctx.guild.id, "ved": member.id, "id": member.id, "name": member.display_name, "role": 0, "del": 1, "night": 0, "nicks": 0, "leader": 1})
        await member.edit(nick = '[MAFIA]: Ведущий')
        str_a = ''.join(get_role)
        embed = discord.Embed(description = f'**Список игроков и их ролей:**\n{str_a}\n\n\n> **Все команды и правила мафии описаны в команде `/help`(3-я страница)**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        embed.set_author(name = 'Информация для нового ведущего', url = 'https://vk.com/dollarbabys', icon_url = 'https://sun9-36.userapi.com/c854428/v854428073/228488/tvUKvnDpcdk.jpg')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        try:
            await member.send(embed = embed)
        except:
            pass
        return await ctx.send(embed = discord.Embed(title = 'Мафия', description = f'**{ctx.author}, Вы успешно передали права ведущего мафиии пользователю {member.mention}**', colour = 0xFB0E14), delete_after = 10)

    @commands.command(aliases = ['gamerole'])
    async def get_roles(self, ctx):
        global get_role
        global game

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if not game == 1:
            return

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return

        str_a = ''.join(get_role)
        embed = discord.Embed(description = f'**Список игроков:**\n{str_a}\n\n**Все команды и правила мафии описаны в команде /help(3-я страница)**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        try:
            await ctx.author.send(embed = embed)
        except discord.Forbidden:
            return await ctx.send(f'`[ERROR]` {ctx.author.mention}, `у вас закрыт доступ к отправке личных сообщений!`', delete_after = 5)

    @commands.command(aliases = ['ночь'])
    async def night(self, ctx):
        global get_role
        global game

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        mchannel = self.bot.get_channel(806215020333236244)

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return
        if bmafia.find_one({"leader": 1})["night"] == 1:
            return await ctx.send('`[ERROR]` `В данный момент уже установлен режим "Ночь"!`', delete_after = 5)

        vhannel = self.bot.get_channel(806214892012830770)
        for f in vhannel.members:
            if bmafia.count_documents({"id": f.id}) == 1 and not bmafia.find_one({"leader": 1})["ved"] == f.id:
                if bmafia.find_one({"id": f.id})["active"] == 1:
                    await f.edit(mute = True)
        
        uch = discord.utils.get(ctx.guild.roles, id = 914455571741167646)
        await mchannel.set_permissions(uch, send_messages = False, read_message_history = True, read_messages = True)
        bmafia.update_one({"id": ctx.author.id}, {"$set": {"night": 1}})
        return await mchannel.send(embed = discord.Embed(description = '**В городе наступает тёмная и страшная ночь. Микрофоны участников были выключены.**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()))
    
    @commands.command(aliases = ['день'])
    async def day(self, ctx):
        global get_role
        global game

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        mchannel = self.bot.get_channel(806215020333236244)

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return
        if bmafia.find_one({"leader": 1})["night"] == 0:
            return await ctx.send('`[ERROR]` `В данный момент уже установлен режим "День"!`', delete_after = 5)

        vhannel = self.bot.get_channel(806214892012830770)
        for f in vhannel.members:
            if bmafia.count_documents({"id": f.id}) == 1 and not bmafia.find_one({"leader": 1})["ved"] == f.id:
                if bmafia.find_one({"id": f.id})["active"] == 1:
                    await f.edit(mute = False)
        
        uch = discord.utils.get(ctx.guild.roles, id = 914455571741167646)
        await mchannel.set_permissions(uch, send_messages = True, read_message_history = True, read_messages = True)
        bmafia.update_one({"id": ctx.author.id}, {"$set": {"night": 0}})
        return await mchannel.send(embed = discord.Embed(description = '**Ночь прошла, наступает утро. Микрофоны участников были включены.**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        global players
        global force
        global prov
        global messageid
        global delb

        ast = 0

        if member.guild == None:
            return

        if not member.guild.id == 477547500232769536:
            return

        if messageid == 0:
            return

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

            if before.channel.id == 806214892012830770:
                ast = 1

        elif not before.channel == None:
            if before.channel.id == 806214892012830770:
                ast = 1

        elif after.channel == None:
            if not before.channel == None:
                if before.channel.id == 806214892012830770:
                    ast = 1

        if ast == 1:
            if not prov == 0:
                if not f'\n<@!{member.id}>' in force:
                    return

                if bmafia.count_documents({"id": member.id}) == 1:
                    if member.id == bmafia.find_one({"mesid": messageid})["ved"]:
                        return

                    mes = await self.bot.get_channel(messageid).fetch_message(bmafia.find_one({"mesid": messageid})["meschan"])
                    force.remove(f'\n<@!{member.id}>')
                    str_a = ''.join(force)
                    if len(force) == 0:
                        embed = discord.Embed(title = 'Игра в мафию', description = f'**Ведущий: <@!{bmafia.find_one({"mesid": messageid})["ved"]}>**\n**Пользователей нет.**', colour = 0xFB9E14, timestamp = mes.created_at)
                    else:
                        if len(force) == 10:
                            source = 'Нет'
                        else:
                            source = f'{10 - len(force)}\nНажмите ✔️ что бы принять участие!'
                        embed = discord.Embed(title = 'Игра в мафию', description = f'**Ведущий: <@!{bmafia.find_one({"mesid": messageid})["ved"]}>**\n**Пользователи:** {str_a}\n**Свободых мест: {source}**', colour = 0xFB9E14, timestamp = mes.created_at)
                        embed.set_footer(text = f'❌ - Отменить | ▶️ - Запустить | ❔ - Проверить')
                    await mes.edit(embed = embed) 
                    players.remove(member.id)
                    delb = member.id
                    return await self.bot.http.remove_reaction(bmafia.find_one({"mesid": messageid})["meschan"], messageid, '✔️', member.id)
            else:
                return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.guild.id == 477547500232769536:
            return

        if before.display_name == after.display_name:
            return

        async for entry in before.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_update):
            if entry.user.bot:
                return
        
        if discord.utils.get(before.guild.roles, id = 914455571741167646) in after.roles:
            await after.edit(nick = before.display_name)     


def setup(bot):
    bot.add_cog(mafia(bot))

    
