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
import urllib
from pymongo import MongoClient
 
cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
report = db["report"]
moder = db["moder"]
rolef = db["role"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

def add(member: discord.Member, arg):
  if moder.count_documents({"guild": 477547500232769536, "id": member.id}) == 0:
    moder.insert_one({"guild": 477547500232769536, "id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0, "x2": 0})
    moder.update_one({"guild": 477547500232769536, "id": member.id}, {"$set": {arg: 1}})
  else:
    moder.update_one({"guild": 477547500232769536, "id": member.id}, {"$set": {arg: moder.find_one({"guild": 477547500232769536, "id": member.id})[arg] + 1}})


global uje 
uje = []

global meid
meid = []

global RCH
RCH = ['Пра', 'ФСБ', 'ГУВД', 'РУВД', 'ПЭ', 'МЗ', 'ПЛ', 'Армия', 'ТСР', 'ЦБ', 'НГ', 'РОВД', 'МРЭО', 'КМ', 'ФМ', 'СТ', 'СБ', 'РМ', 'УМ', 'ЧК']

class role(commands.Cog):
    """ROLE Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Role State by dollar ム baby#3603 - Запущен')

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        author = ctx.message.author

        user = ctx.message.author if (member == None) else member
        embed = discord.Embed( description = f'''{author.mention}, вот аватар пользователя {user.mention}:''', color= 0xFB9E14)
        embed.set_image(url=user.avatar_url_as(format = None, size = 4096))
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def allsn(self, ctx, member: discord.Member):
        number = 0
        mas = [ ]
        for i in rolef.find({"is_active": 2, "leader": member.id}):
            channel = self.bot.get_channel(i["kuda"])
            message = await channel.fetch_message(i["message_id"])
            await message.delete()
            rol = ctx.guild.get_role(i["role_id"])
            chan = self.bot.get_channel(i["channel"])
            membs = discord.utils.get(ctx.guild.members, id = i["leader"])
            membr = discord.utils.get(ctx.guild.members, id = i["user_id"])
            try:
                await membr.remove_roles(rol)
                number += 1
                await chan.send(f'`[ACCEPT]` {ctx.author.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {membr.display_name}, с ID: {membr.id}`')
                mas.append(f'[ACCEPT №{number}]  | {ctx.author.display_name} одобрил снятие роли ({rol.name}) от {membs.display_name}, пользователю {membr.display_name}, с ID: {membr.id}\n')
                rolef.delete_one({"_id": i["_id"]})
                add(ctx.author, "derols")
            except:
                pass
        obfile = open(f'{member.id}.txt', 'w', encoding='utf-8')
        obfile.write(f'[System]: Начался процесс снятия ролей по формам {member.display_name}\n\n')
        
        str_a = ''.join(mas)
        try:
            obfile.write(f'{str_a}\n\n')
        except:
            pass
        obfile.write(f'[System]: По формам {member.display_name}({member}) было снято {number} ролей.')
        obfile.close()

        await ctx.send(embed = discord.Embed(description = f'💎 Выполнены все формы от пользователя {member.mention}`({member})`\n\n`Действия сохранены в системном файле`',colour=0xFB9E14),file=discord.File(fp=f'{member.id}.txt'))
        os.remove(f'{member.id}.txt')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == f'<@!{self.bot.user.id}>' or  ctx.content == f'<@{self.bot.user.id}>':
            #await ctx.channel.send(f'{ctx.author.mention},', embed = discord.Embed(title = 'Основная информация', description = f'**Привет! Меня зовут Rodina RP бот.\nСоздатель бота: adminhelper#777\n\n> `Префикс установленный на этом сервере:`    /\n> `Ссылка на добавление бота:` https://discord.com/api/oauth2/authorize?client_id=729309765431328799&permissions=8&scope=bot\n\n`Информация о боте -` /botinfo\n`Информация по командам -` /help**', colour = 0xFB9E14), delete_after = 20)
            return

        global uje
        role_registr = ['!роль', 'роль', 'Роль', '!Роль']
        nick_registr = ['Пра-во', 'РОВД', 'Банк', 'ФСБ', 'РУВД', 'ГУВД', 'Армия', 'ТСР', 'МРЭО', 'НГ-А', 'НГ-Л', 'МЗ-А', 'МЗ-Э', 'Судья', 'КМ', 'ФМ', 'СТ', 'СБ', 'РМ', 'УМ', 'ЧК'] # Сюда вообще все теги добавь, если там что-то новое будет, если заменят, удаляй то, чего больше нету и вставляй новое, так же.
        gos = ['Пра-во', 'РОВД', 'Банк', 'ФСБ', 'РУВД', 'ГУВД', 'МРЭО', 'Армия', 'ТСР', 'НГ-А', 'НГ-Л', 'МЗ-А', 'МЗ-Э', 'Судья'] # Сюда все теги госов, по такому же принципу, если вдруг новые появятся 
        opg = ['КМ', 'ФМ', 'СТ', 'СБ', 'РМ', 'УМ', 'ЧК'] 
 

        ROLES = {
            'Пра-во': 478970291444383766,
            'РОВД': 848630088170078269,
            'Банк': 848658294759227392,
            'ФСБ': 848660081222483988,
            'РУВД': 848661195166842900,
            'ГУВД': 848663860399046666,
            'Армия': 848664593524850748,
            'ТСР': 848971714858844191,
            'НГ-А': 848973072006512676,
            'НГ-Л': 862361473988821012,
            'МЗ-А': 848974272541622362,
            'МРЭО': 860207024930160680,
            'МЗ-Э': 848977375093325844,
            'Судья': 848977843228115024,
            'ФМ': 479048866704916540,
            'КМ': 479198132211548161,
            'СТ': 479049028705976340,
            'СБ': 479049200768647169,
            'РМ': 479198415578988554,
            'УМ': 479198488563810315,
            'ЧК': 479185785510166567,
        }

        if not ctx.author.bot:
            if not ctx.guild:
                for i in rolef.find({"user_id": ctx.author.id}):
                    if not i["zaproschannel"] == 0:
                        if ctx.attachments == []:
                            return
                        else:
                            chanel = self.bot.get_channel(i["zaproschannel"])
                            guild = self.bot.get_guild(477547500232769536)
                            member = discord.utils.get(guild.members, id = i["user_id"])
                            message = await self.bot.get_channel(i["zaproschannel"]).fetch_message(i["message_id"])
                            if i["leader"] > 1:
                              embed = discord.Embed(description = f'`Discord >> Проверка на валидность никнейма`\n`[NOTIFICATION]` `Внимаение, в нике указан старший ранг, обязательно просмотрите его статистику!`', colour = 0xFB9E14, timestamp = message.created_at)
                            else:
                              embed = discord.Embed(description = '`Discord >> Проверка на валидность никнейма`', colour = 0xFB9E14, timestamp = message.created_at)
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {ctx.author.mention}', inline = True)
                            embed.add_field(name = 'Никнейм', value = f'`Ник:` {ctx.author.display_name}', inline = True)
                            if i["leader"] > 1:
                              embed.add_field(name = 'Роли для выдачи', value = f'`Роли для выдачи`: {discord.utils.get(guild.roles, id = i["role_id"]).mention} `и` {discord.utils.get(guild.roles, id = i["leader"]).mention}', inline = False)
                            else:
                              embed.add_field(name = 'Роль для выдачи', value = f'`Роль для выдачи`: {discord.utils.get(guild.roles, id = i["role_id"]).mention}', inline = False)
                            embed.add_field(name = 'Отправлено с канала', value = f'{self.bot.get_channel(i["zaproschannel"]).mention}', inline = False)
                            if i["leader"] > 1:
                              embed.add_field(name = 'Действия', value = '`[✔️] - выдать роли старшего состава и организации.`\n`[➕] - Выдать роль организации`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`\n`[❔] - Запросить скрин-шот статистики`\n`[✏️] - Установить пользователю Nick_Name`')
                            else:
                              embed.add_field(name = 'Действия', value = '`[✔️] - выдать роль.`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`\n`[❔] - Запросить скрин-шот статистики`\n`[✏️] - Установить пользователю Nick_Name`')
                            embed.set_image(url = ctx.attachments[0].url)
                            await message.edit(embed = embed)
                            embed1 = discord.Embed(description = f'**Скриншот прикреплён к изначальному [сообщению-запросу]({message.jump_url}).**', colour = 0xFB9E14) 
                            mesg = await chanel.send(f'`[UPDATE]` `Пользователь {member.display_name}`({member.mention}) `отправил доказательства на получение роли!`', embed = embed1)
                            rolef.update_one({"id": ctx.author.id}, {"$set": {"zaproschannel": 0, "prufid": mesg.id}})
                            await ctx.author.send('`[SUCCESFULL] Ваши доказательства отправлены в необходимый канал`')
                            return
                            
            elif not ctx.guild.id == 477547500232769536:
                return
            
        msg = ctx.content.lower()

        if 'снять роль у' in msg:
          if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return
          check = ctx.raw_mentions
          if check == None:
              return
          else:
              member = ctx.guild.get_member(check[0])
          if not ctx.channel.id == 704050836258422854:
              await ctx.delete()
              return await ctx.channel.send(embed = discord.Embed(description = f'**❌ {ctx.author.name}, запросы разрешено отправлять только из канала <#704050836258422854>!**', colour = 0xFB9E14), delete_after = 5)
          role_checkers = [862361473988821012, 860207024930160680, 479048866704916540, 478970291444383766, 848630088170078269, 848658294759227392, 848660081222483988, 848661195166842900, 848663860399046666, 848664593524850748, 848971714858844191, 848973072006512676, 848974272541622362, 848977375093325844, 848977843228115024, 479198132211548161, 479049028705976340, 479049200768647169, 479198415578988554, 479198488563810315, 479185785510166567]
          z = 0
          for i in member.roles:
            if i.id in role_checkers:
              z = i.id
              break
          if z == 0:
            return await ctx.channel.send('`[ERROR]` `Данный пользователь не имеет фракционных ролей!`', delete_after = 5)

          if rolef.count_documents({"user_id": member.id}) == 1 and rolef.find_one({"user_id": member.id})["is_active"] == 2:
              await ctx.add_reaction('❌')
              return await ctx.channel.send(f'{ctx.author.mention}, `уже создана заявка на снятие роли у этого пользователя.`', delete_after = 5)

          msg1 = await ctx.channel.send('`Введите причину снятия роли в чат`')
          def checkms(m):
            return m.author == ctx.author and m.channel == ctx.channel
          try:
              msg2 = await self.bot.wait_for('message', timeout = 30.0, check = checkms)
          except Exception:
              await msg1.delete()
              return
          await msg1.delete()
          reas = msg2.content
          await msg2.delete()

          channel, nad_role = self.bot.get_channel(505009452571820032), discord.utils.get(ctx.guild.roles, id=z)
          
          embed = discord.Embed(description = '`Discord >> Запрос на снятие роли`', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
          embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
          embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {member.mention}', inline = True)
          embed.add_field(name = 'Никнейм', value = f'`Ник:` {member.display_name}', inline = True)
          embed.add_field(name = 'Отправил', value = f'`Модератор:` {ctx.author.mention}', inline = False)
          embed.add_field(name = 'По причине', value = f'`По причине:` {reas}', inline = True)
          embed.add_field(name = 'Роль для снятия', value = f'`Роль для снятия`: {nad_role.mention}', inline = False)
          embed.add_field(name = 'Отправлено с канала', value = f'{ctx.channel.mention}', inline = False)
          embed.add_field(name = 'Действия', value = '`[✔️] - снять роль.`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`')
          embed.set_image(url = member.avatar_url)
          message = await channel.send(embed = embed)
          rolef.insert_one({"user_id": member.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 2, "channel": ctx.channel.id, "leader": ctx.author.id, "kuda": channel.id})
          await message.add_reaction('✔️')
          await message.add_reaction('❌')
          await message.add_reaction('🇩')

          add(ctx.author, "dezaprols")
          return await ctx.add_reaction('📨')

        if msg in role_registr:
            ak = ctx.author.display_name.replace('[', '')
            ak1 = ak.replace(']', '')
            ak2 = ak1.split()
            if not ctx.channel.id == 815924842984898590:
                await ctx.delete()
                return await ctx.channel.send(embed = discord.Embed(description = f'**❌ {ctx.author.name}, получать роли нужно только в канале <#815924842984898590>!**', colour = 0xFB9E14), delete_after = 5)

            ath = ctx.author.display_name.split(' ')
            for z in ath:
                if z.replace('[', '').replace(']', '') in nick_registr:
                    z = z.replace('[', '').replace(']', '')
                    break

            if not z in nick_registr:
                await ctx.delete()
                if ctx.author.id in uje:
                    return

                embed = discord.Embed(title = 'Получение ролей', description = f'**В Вашем ник-нэйме указан не верный тэг!\n`Discord >> Список всех фракционных тэгов`**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                embed.add_field(name = f'**Тэги Государственных Организаций:**', value = f'> `Пра-во, РОВД, Банк, ФСБ, РУВД, ГУВД, Армия, ТСР, НГ-А, МЗ-А, МЗ-Э, Судья`')
                embed.add_field(name = f'**Дополнительные тэги Нелегальных Организаций**', value = f'> `ФМ, СТ, СБ, ЧК, УМ, КМ, РМ`')
                embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                embed.set_thumbnail(url = ctx.guild.icon_url)
                await ctx.channel.send(embed = embed, delete_after = 25)
                await asyncio.sleep(60)

            if z in nick_registr:
                if rolef.count_documents({"user_id": ctx.author.id}) == 1 and rolef.find_one({"user_id": ctx.author.id})["is_active"] == 1:
                    await ctx.add_reaction('🕐')
                    return await ctx.channel.send(f'{ctx.author.mention}, `Вы уже отправили своё заявление на получение роли, дождитесь его одобрения.`', delete_after = 5)

                channel = self.bot.get_channel(505009452571820032)
                lidrole = 1
                if ROLES[z] == 1703:
                    return await ctx.channel.send(embed = discord.Embed(title = 'Замороженная организация', description = f'**Организация указанная в вашем ним-нэйме заморожена.**', colour = 0xFB9E14), delete_after = 5) 

                nad_role = discord.utils.get(ctx.guild.roles, id=ROLES[z])
                if '10/10' in ak2:
                  if z in gos:
                    lidrole = discord.utils.get(ctx.guild.roles, id = 800640188807118858)
                  elif z in opg:
                    lidrole = discord.utils.get(ctx.guild.roles, id = 800640178800295946)
                elif '9/10' in ak2:
                  if z in gos:
                    lidrole = discord.utils.get(ctx.guild.roles, id = 800639571003179068)
                  elif z in opg:
                    lidrole = discord.utils.get(ctx.guild.roles, id = 800639550186979338)
                
                if '9/10' in ak2:
                  embed = discord.Embed(description = '`Discord >> Проверка на валидность никнейма`\n`[NOTIFICATION]` `Внимаение, в нике указан 9-й ранг, обязательно просмотрите его статистику!`', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                if '10/10' in ak2:
                  embed = discord.Embed(description = '`Discord >> Проверка на валидность никнейма`\n`[NOTIFICATION]` `Внимаение, в нике указан 10-й ранг, обязательно просмотрите его статистику!`', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                else:
                  embed = discord.Embed(description = '`Discord >> Проверка на валидность никнейма`', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {ctx.author.mention}', inline = True)
                embed.add_field(name = 'Никнейм', value = f'`Ник:` {ctx.author.display_name}', inline = True)
                if not lidrole == 1:
                  embed.add_field(name = 'Роли для выдачи', value = f'`Роли для выдачи`: {nad_role.mention} `и` {lidrole.mention}', inline = False)
                else:
                  embed.add_field(name = 'Роль для выдачи', value = f'`Роль для выдачи`: {nad_role.mention}', inline = False)
                embed.add_field(name = 'Отправлено с канала', value = f'{ctx.channel.mention}', inline = False)
                if not lidrole == 1:
                  embed.add_field(name = 'Действия', value = '`[✔️] - выдать роли старшего состава и организации.`\n`[➕] - Выдать роль организации`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`\n`[❔] - Запросить скрин-шот статистики`\n`[✏️] - Установить пользователю Nick_Name`')
                else:
                  embed.add_field(name = 'Действия', value = '`[✔️] - выдать роль.`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`\n`[❔] - Запросить скрин-шот статистики`\n`[✏️] - Установить пользователю Nick_Name`')
                embed.set_image(url = ctx.author.avatar_url)

                if nad_role in ctx.author.roles:
                    await ctx.channel.send(f'{ctx.author.mention}, `у вас уже есть роль` {nad_role.mention}', delete_after = 5)
                    return await ctx.add_reaction('❌')

                await ctx.add_reaction('📨')

                message = await channel.send(embed = embed)
                await message.add_reaction('✔️')

                if not lidrole == 1:
                    rolef.insert_one({"user_id": ctx.author.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 1, "channel": ctx.channel.id, "leader": lidrole.id, "pruf": 0, "zaproschannel": 0, "prufid": 0, "zapid": 0, "kuda": channel.id, "setn": 0})
                    await message.add_reaction('➕')
                else:
                    rolef.insert_one({"user_id": ctx.author.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 1, "channel": ctx.channel.id, "leader": 0, "pruf": 0, "zaproschannel": 0, "prufid": 0, "zapid": 0, "kuda": channel.id, "setn": 0})
                await message.add_reaction('❌')
                await message.add_reaction('🇩')
                await message.add_reaction('❔')
                await message.add_reaction('✏️')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global meid
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
            return
        if not payload.guild_id == 477547500232769536:
                return
        
        role_checkers = [478970291444383766, 848630088170078269, 848658294759227392, 848660081222483988, 848661195166842900, 848663860399046666, 848664593524850748, 848971714858844191, 848973072006512676, 848974272541622362, 848977375093325844, 848977843228115024, 479198132211548161, 479049028705976340, 479049200768647169, 479198415578988554, 479198488563810315, 479185785510166567]
        chal = [505009452571820032]

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id in chal:
                return
            message = await channel.fetch_message(payload.message_id)
            memb = payload.member
            emoji = str(payload.emoji)
                
            if rolef.count_documents({"message_id": message.id}) == 0:
                await message.delete()
                return await channel.send(f'`[BUGTRAKER]` {memb.mention} `удалил багнутый запрос`')

            for i in rolef.find({"message_id": message.id}):
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(i["user_id"])  
                chan = self.bot.get_channel(i["channel"])
                if member == None:
                    await message.delete()
                    await channel.send(f'`[BUGTRAKER]` {memb.mention} `запрос был багнутым, мне пришлось его удалить. ID Удалённого запроса: {i["user_id"]}`')
                    return rolef.delete_one({"message_id": message.id})
                if i["is_active"] == 1 or i["is_active"] == 2:
                    if emoji == '❔':
                        if i["pruf"] == 0:
                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `запрашивает у вас статистику игрового аккаунта, отправьте в личные сообщения боту скриншот [/stats + /time]`')
                            serf = await channel.send(f'`[PRUF]` {memb.mention} `запросил доказательства от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.update_one({"message_id": message.id}, {"$set": {"pruf": 1, "zaproschannel": channel.id, "zapid": serf.id}})
                            await member.send(f'{member.mention}, `модератор {memb.display_name} запрашивает у вас статистику игрового аккаунта, отправьте в личные сообщения боту скриншот [/stats + /time]`')
                        else:
                            await channel.send(f'`[ERROR]` {memb.mention}, `статистику запросил другой модератор.`', delete_after = 5)
                    if emoji == '✏️':
                        if i["setn"] == 0:
                            rolef.update_one({"message_id": message.id}, {"$set": {"setn": 1}})
                            mes1 = await channel.send(f'{memb.mention}, `введите ник-нейм который хотите установить в чат.`')
                            def check(m):
                                return m.author.id == memb.id and m.channel.id == channel.id
                            try:
                                msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                            except Exception:
                                await channel.send(f'{memb.mention}, `Время установки НикНэйма вышло`', delete_after = 5)
                                await mes1.delete()
                                try:
                                    await self.bot.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                                    rolef.update_one({"message_id": message.id}, {"$set": {"setn": 0}})
                                except:
                                    pass
                            if len(list(msg.content)) > 32:
                                await channel.send(f'{memb.mention}, `Вы превысили допустимый лимит символов: {len(list(msg.content))}/32`', delete_after = 5)
                                await msg.delete()
                                await mes1.delete()
                                try:
                                    await self.bot.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                                    rolef.update_one({"message_id": message.id}, {"$set": {"setn": 0}})
                                except:
                                    pass
                            else:
                                await member.edit(nick = msg.content)
                                await channel.send(f'`[INFO]` `Модератор` {memb.mention} `установил пользователю` {member.mention} `ник: {msg.content}`')
                                await member.send(f'{member.mention}, `модератор {memb.display_name} установил Вам следующий ник: {msg.content}`\n`Если вы считаете, что данный ник является недопустимым, напишите жалобу на форум:` https://forum.robo-humster.ru/')
                                await msg.delete()
                                await mes1.delete()
                                await self.bot.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                                rolef.update_one({"message_id": message.id}, {"$set": {"setn": 0}})
                        else:
                            await channel.send(f'`[ERROR]` {memb.mention}, `данному пользователю уже меняют ник`', delete_after = 5)

                    elif emoji == '➕':
                        for role in member.roles:
                            if role.id in role_checkers:
                                await member.remove_roles(role)
                            else:
                                pass
                        
                        if not i["prufid"] == 0:
                            msg = await channel.fetch_message(i["prufid"])
                            await msg.delete()

                        if not i["zapid"] == 0:
                            msg1 = await channel.fetch_message(i["zapid"])
                            await msg1.delete()
                        
                        await member.add_roles(self.bot.get_guild(payload.guild_id).get_role(i["role_id"]))
                        await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу роли.`\n`Роль` <@&{i["role_id"]}> `была выдана!`')
                        await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                        rolef.delete_one({"message_id": message.id})
                        add(memb, "rols")
                        return await message.delete()
                        
                    elif emoji == '✔️':                          
                        if i["is_active"] == 1:              
                            for role in member.roles:
                                if role.id in role_checkers:
                                    await member.remove_roles(role)
                                else:
                                    pass
                            
                            if not i["prufid"] == 0:
                                msg = await channel.fetch_message(i["prufid"])
                                await msg.delete()

                            if not i["zapid"] == 0:
                                msg1 = await channel.fetch_message(i["zapid"])
                                await msg1.delete()

                            if i["leader"] > 1:
                                await member.add_roles(self.bot.get_guild(payload.guild_id).get_role(i["role_id"]))
                                await member.add_roles(self.bot.get_guild(payload.guild_id).get_role(i["leader"]))
                                await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу фракционных ролей.`\n`Роли` <@&{i["role_id"]}> `и` <@&{i["leader"]}> `были выданы!`')
                            else:
                                await member.add_roles(self.bot.get_guild(payload.guild_id).get_role(i["role_id"]))
                                await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу роли.`\n`Роль` <@&{i["role_id"]}> `была выдана!`')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})
                            add(memb, "rols")
                            return await message.delete()
                        elif i["is_active"] == 2:
                            membs = self.bot.get_guild(payload.guild_id).get_member(i["leader"])
                            if membs.id == memb.id:
                                return
                            
                            await message.delete()
                            rol = self.bot.get_guild(payload.guild_id).get_role(i["role_id"])
                            await chan.send(f'`[ACCEPT]` {memb.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {member.display_name}, с ID: {member.id}`')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {member.display_name}, с ID: {member.id}`')
                            await member.remove_roles(rol)
                            rolef.delete_one({"message_id": message.id})
                            add(memb, "derols")
                    elif emoji == '❌':
                        if i["is_active"] == 1:
                            await message.delete()
                            if not i["prufid"] == 0:
                                msg = await channel.fetch_message(i["prufid"])
                                await msg.delete()

                            if not i["zapid"] == 0:
                                msg1 = await channel.fetch_message(i["zapid"])
                                await msg1.delete()

                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на выдачу роли.`\n`Ваш ник при отправке: {member.display_name}`\n`Установите ник на: [Фракция Ранг/10] Имя_Фамилия\nАватар фракции можно найти с помощью команды +photo <фракция>`')
                            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})
                        elif i["is_active"] == 2:
                            member = self.bot.get_guild(payload.guild_id).get_member(i["leader"])
                            await message.delete()
                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на снятие роли у пользователя` {member.mention}')
                            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})
                    elif emoji == '🇩':
                        await message.delete()
                        if i["is_active"] == 1:
                            if not i["prufid"] == 0:
                                msg = await channel.fetch_message(i["prufid"])
                                await msg.delete()

                            if not i["zapid"] == 0:
                                msg1 = await channel.fetch_message(i["zapid"])
                                await msg1.delete()

                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на выдачу роли.`\n`Ваш ник при отправке: {member.display_name}`\n`Установите ник на: [Фракция Ранг/10] Имя_Фамилия\nАватар фракции можно найти с помощью команды +photo <фракция>`')
                            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})
                        elif i["is_active"] == 2:
                            member = self.bot.get_guild(payload.guild_id).get_member(i["leader"])
                            if member.id == memb.id:
                                await channel.send(f'`[DENY]` {memb.mention} `удалил свой запрос`')
                            else:
                                await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на снятие роли у пользователя` <@!{i["user_id"]}>`.`')
                                await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})

def setup(bot):
    bot.add_cog(role(bot))
