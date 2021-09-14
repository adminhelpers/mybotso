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
import sqlite3
import asyncio
import json
import requests
import jishaku
from pymongo import MongoClient
from discord_buttons_plugin import *

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["RodinaBD"]
reports = db["reports"]

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
dbd = cluster["rodina"]
event = dbd["eventman"]

clusterf = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
dbf = clusterf["rodina"]
report = dbf["report"]
moder = dbf["moder"]
rolef = dbf["role"]

cl = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
dbtest = cl["rodinaname"]
family = dbtest["famacoll"]

clss = MongoClient("mongodb+srv://bot:50TKFaQiSaIMKiiO@cluster0.orxb3.mongodb.net/phoenix?retryWrites=true&w=majority")
dbstest = clss["phoenix"]
familys = dbstest["famacoll"]

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
RCH = ['Пра-во', 'ФСБ', 'ГИБДД', 'ГУВД', 'ПЭ', 'МЗ', 'ПЛ', 'Армия', 'ТСР', 'ЦБ', 'НГ', 'РОВД', 'МРЭО', 'КМ', 'ФМ', 'СТ', 'СБ', 'РМ', 'УМ', 'ЧК']

global role_checkers
role_checkers = [478970291444383766, # ★ Правительство ★
                848658294759227392, # ★ Центральный Банк ★
                860207024930160680, # ★ МРЭО ★
                848660081222483988, # ★ Федеральная служба безопасности ★
                848663860399046666, # ★ Государственная Инспекция Безопасности Дорожного Движения ★
                848661195166842900, # ★ Главное Управление Внутренних Дел ★
                848630088170078269, # ★ Районное Отделение Внутренних Дел ★
                848664593524850748, # ★ Армия ★
                848971714858844191, # ★ Тюрьма Строгого Режима ★
                848973072006512676, # ★ Новостное Агенство г.Арзамас ★
                848974272541622362, # ★ Министерство Здравоохранения г.Арзамас ★
                848977375093325844, # ★ Министерство Здравоохранения г.Эдово ★
                848977843228115024, # ★ Судья ★
                479048866704916540, # ★ Фантомасы ★
                479049028705976340, # ★ Санитары ★
                479049200768647169, # ★ Солнцевская Братва ★
                479185785510166567, # ★ Чёрная Кошка ★
                479198132211548161, # ★ Кавказская Мафия ★
                479198415578988554, # ★ Русская Мафия ★
                479198488563810315] # ★ Украинская Мафия ★

global nick_registr
nick_registr = ['Пра-во', 'Банк', 'МРЭО', 'ФСБ', 'ГИБДД', 'ГУВД', 'РОВД', 'Армия', 'ТСР', 'НГ-А', 'МЗ-А', 'МЗ-Э', 'Судья', 'ФМ', 'СТ', 'СБ', 'ЧК', 'КМ', 'РМ', 'УМ']

global gos
gos = ['Пра-во', 'Банк', 'МРЭО', 'ФСБ', 'ГИБДД', 'ГУВД', 'РОВД', 'Армия', 'ТСР', 'НГ-А', 'МЗ-А', 'МЗ-Э', 'Судья'] 

global opg  
opg = ['КМ', 'РМ', 'УМ', 'ФМ', 'СТ', 'СБ', 'ЧК'] 

global ROLES
ROLES = {
  'Пра-во': 478970291444383766, # ★ Правительство ★
  'Банк': 848658294759227392, # ★ Центральный Банк ★
  'МРЭО': 860207024930160680, # ★ МРЭО ★
  'ФСБ': 848660081222483988, # ★ Федеральная служба безопасности ★
  'ГИБДД': 848663860399046666, # ★ Государственная Инспекция Безопасности Дорожного Движения ★
  'ГУВД': 848661195166842900, # ★ Главное Управление Внутренних Дел ★
  'РОВД': 848630088170078269, # ★ Районное Отделение Внутренних Дел ★
  'Армия': 848664593524850748, # ★ Армия ★
  'ТСР': 848971714858844191, # ★ Тюрьма Строгого Режима ★
  'НГ-А': 848973072006512676, # ★ Новостное Агенство г.Арзамас ★
  'МЗ-А': 848974272541622362, # ★ Министерство Здравоохранения г.Арзамас ★
  'МЗ-Э': 848977375093325844, # ★ Министерство Здравоохранения г.Эдово ★
  'Судья': 848977843228115024, # ★ Судья ★
  'ФМ': 479048866704916540, # ★ Фантомасы ★
  'СТ': 479049028705976340, # ★ Санитары ★
  'СБ': 479049200768647169, # ★ Солнцевская Братва ★
  'ЧК': 479185785510166567, # ★ Чёрная Кошка ★
  'КМ': 479198132211548161, # ★ Кавказская Мафия ★
  'РМ': 479198415578988554, # ★ Русская Мафия ★
  'УМ': 479198488563810315} # ★ Украинская Мафия ★
    

async def get_prefix(bot, message):
    if message.guild == None:
        return
    guildid = int(message.guild.id) 
    if reports.count_documents({"guild_id": guildid, "proverka": 1}) == 0:
        return "!"
    return reports.find_one({"guild_id": guildid, "proverka": 1})["prefix"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = get_prefix, intents=intents)
buttons = ButtonsClient(bot)
bot.load_extension('jishaku')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Основа бота включена.')

#bot.load_extension('cogs.voice')
bot.load_extension('cogs.moderation')
#bot.load_extension('cogs.funny')
#bot.load_extension('cogs.role')
bot.load_extension('cogs.mafia')
bot.load_extension('cogs.privats')
#bot.load_extension('cogs.req')
bot.load_extension('cogs.golosovanie')
bot.load_extension('cogs.economy')
#bot.load_extension('cogs.otdeli')
#bot.load_extension('cogs.gov')
bot.load_extension('cogs.family')
bot.load_extension('cogs.forma')
bot.load_extension('cogs.eventmanager')
bot.load_extension('cogs.debug')


@bot.command()
@commands.is_owner()
async def recog(ctx, *, name = None):
    bot.reload_extension(f'cogs.{name}')
    e = discord.Embed(title = 'Перезагрузка Cog-Ассигмента', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
    e.add_field(name = '<:python:736561225743466556> `Перезагрузка кога`', value = f'**Reboot Module => {name}**')
    e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    return await ctx.send(embed = e)

@bot.command()
@commands.is_owner()
async def fullstek(ctx):
    jsp = {815924842984898590:"『📩』запрос-роли", 478171270664421376:"『💬』общение", 675591633013571604:"『🪁』проверка-уровня", 818222772215349328:"『💰』казино", 826863776274972712:"『🎤』медиа", 477875131302019105:"『📋』новости-сервера", 800038891611619388:"『📢』новости-discord", 816051676846358569:"『 🚩』information", 507835714109571072:"『📌』правила", 817815183094448130:"『📍』support", 594257934553448454:"『💬』модераторская", 704050836258422854:"『💬』снятие-роли", 505009452571820032:"『💬』requests-for-roles", 650296921247973376:"『💬』test-channel", 817814608668655627:"『❕』логи-репорта", 800083559409909810:"『💬』выдача-наказаний", 834039427541631016:"『💬』модерские-логи", 804466619963277382:"『🎴』Ожидание обзвона", 804466357479407616:"『👹』Обзвон на пост модератора", 723583118665056307:"『🌍』Модераторская", 804465926132203540:"『🌍』Собрание модераторов", 804466055061176350:"『🤡』Казнь модераторов", 776096903032733716:"『👥』Тет-А-Тет с Главным Администратором", 697865618715705394:"『🔒』Конференция с Главным администратором", 732361210611367987:"『 🌹 』Стримы :3", 615288302248919040:"『 🔈』Общение [ I ]", 800687294200807485:"『 🔈』Общение [ II ]", 710156619480039424:"『🎭』Друзья с ЖВД", 806485613222166538:"『 📞』Создать приват", 840521240279646218:"『 💡 』логи-заказов", 805487247692005417:"『💸』заказ-услуг", 834856598122922034:"『✨』брифинг", 834856650828677120:"『🚗』заезды", 834856712946712667:"『🌌』чат", 834856760116117615:"『📊』судейство", 834856813262405632:"『📝』регистрация", 834856905925984346:"『🔲』результаты", 834855746101051463:"『📀』Брифинг", 834855881320431616:"『📃』Квалификация", 834855978314235924:"『👥』Парные", 834856391550304326:"『🧣』Тренировка", 806215020333236244:"『🔮』чат-игроков-мафии", 806215783121289297:"『🔮』чат-мафии", 806216885595144223:"『🔮』правила-игры-мафия", 806214892012830770:"『🕵』Мафия", 800308708214308864:"『🎤』караоке", 800307632958603274:"『📃』правила-караоке", 800308338574753822:"『🌟』заявка-на-караоке", 800308767816286229:"『 🔋 』караоке", 809324805819858974:"『👑』элитка", 809325078797090846:"『💎』Канал элитных пользователей", 591642627137339433:"『🔳』family-chat", 809325601751564298:"『🎵』v-i-p-music", 809325772564463636:"『🎵』music", 809325951489802260:"『🎧』Музыкальный канал #1", 809326020943544320:"『🎧』Музыкальный канал #2", 796753871703244805:"『 🔓 』собрание-чат", 615294642325553167:"『 🚩』Глобальная RP.", 615294573224132619:"『 🚩』Собрание.", 671733484435275777:"『📛』общение", 615294630853869579:"『📛』Глобальная RP.", 615294696092336138:"『 🔓 』Переговоры/Обсуждение.", 652918815533039616:"『 🚩』Собрание.", 662334619542224912:"『📃』система-повышения", 662334508300763136:"『📃』отчёты-на-повышение", 662334553611960344:"『📃』общение", 813499409081434162:"『📃』антиблат-правительство", 662334046579327001:"『🎓』Приёмная", 662334427828977694:"『🎓』Правительство [Общий]", 662334318995046423:"『 🔓 』Кабинет Вице - Губернатора", 662334158802124805:"『 🔓 』Кабинет Губернатора", 817808860298346536:"『📃』система-повышения", 817809302881566780:"『📃』отчёты-на-повышение", 817809411623747624:"『📃』общение", 817809536215547934:"『📃』антиблат-прокуратуры", 817807859550388235:"『 ⌛ 』Приемная", 817808039918305330:"『 ⌛ 』Прокуратура г. Лыткарино[Общий]", 819291132533538826:"『 ⌛ 』Кабинет Судей", 817808164308516914:"⌛ | Кабинет Зам. Ген. Прокурора", 817808203777048626:"⌛ | Кабинет Ген. Прокурора", 662360842632953866:"『📃』система-повышения", 662360825402753035:"『📃』отчёты-на-повышение", 662360791525097513:"『📃』общение", 813500702605049896:"『📃』антиблат-банка", 662360525702823936:"『 💲 』Приёмная", 662360587690442867:"『 💲 』Центральный Банк [Общий]", 662360682708336671:"『 🔓 』Кабинет Заместителя Директора Банка", 662360753105272845:"『 🔓 』Кабинет Директора Банка", 662366456230707202:"『📃』система-повышения", 662366443630886912:"『📃』отчёт-на-повышение", 715929240096342016:"『📃』дела-усб", 662366412563546122:"『📃』общение", 813501736672165958:"『📃』антиблат-фсб", 662366235790540800:"『🚨』Приёмная", 662366301435461648:"『🚔』ФСБ [Общий]", 662417111963926558:"『🚔』Патруль №1", 662417142972547112:"『🚓』Патруль №2", 662366356406272011:"『 🔓 』Кабинет Полковника ФСБ", 662366392162582569:"『 🔓 』Кабинет Директора ФСБ", 662367606237298749:"『📃』система-повышения", 662367631298396161:"『📃』отчёты-на-повышение", 662367296500531200:"『📃』общение", 813502466708340736:"『📃』антиблат-гувд", 662367028220395520:"『🕵』Приёмная", 662367200182796288:"『🕵』ГУВД [Общий]", 662417180347858974:"『🚔』Патруль №1", 662417208730714127:"『🚔』Патруль №2", 662367243883118632:"『 🔓 』Кабинет Полковника ГУВД", 662367280470163459:"『 🔓 』Кабинет Генерала ГУВД", 662368381508255756:"система-повыше ния", 662368407286710282:"『📃』отчёты-на-повышение", 662368426374987796:"『📃』общение", 813502938190053446:"『📃』антиблат-гибдд", 662368006344802344:"『🕵』Приёмная", 662368183058956348:"『🕵』ГИБДД [Общий]", 662417241421119543:"『🚔』Патруль №1", 662417269065908277:"『🚔』Патруль №2", 662368272913661999:"『 🔓 』Кабинет Полковника ГИБДД   ", 662368305813651497:"『 🔓 』Кабинет Генерала ГИБДД", 662360048659595294:"『📃』система-повышения", 662360006678675466:"『📃』отчёты-на-повышение", 662359962277642244:"『📃』общение", 813503092968390696:"『📃』антиблат-армия", 662359739425882113:"『💂🏻』Приёмная", 662359846041026591:"『💂🏻』Армия [Общий]", 788853029965135912:"『🔫』Доставка БП", 662359890580209664:"『 🔓 』Кабинет Полковника Армии", 662359926840098826:"『 🔓 』Кабинет Генерала Армии", 662365517083967511:"『📃』система-повышения", 662365505046315018:"『📃』отчёт-на-повышение", 662365473249427476:"『📃』общение", 813504365938999317:"『📃』антиблат-тср", 662365263664119819:"『🚌』Приёмная", 662365345884930118:"『🚬』ТСР [Общий]", 662365404764569650:"『 🔓 』Кабинет Заместителя Начальника ТСР", 662365445944508426:"『 🔓 』Кабинет Начальника ТСР", 662364912106078209:"『📃』система-повышения", 662364895026741279:"『📃』отчёты-на-повышение", 662364858788085800:"『📃』общение", 813504717510148166:"『📃』антиблат-сми-а", 751173546859823165:"『🧭』Н.А.-г.Арзамас[Общий]", 662364689539399699:"『 🔓 』Кабинет Заместителя Директора Н.А. г.Арзамас", 662364560409493572:"『🎥』Приёмная", 662364722749767710:"『 🔓 』Кабинет Директора Н.А. г.Арзамас", 751172900026843299:"система-повышения ", 751173034219667646:"『📃』отчёты-на-повышение", 751173157905367151:"『📃』общение", 813505243404959764:"『📃』антиблат-сми-л", 751173502358388768:"『🎥』Приёмная", 662364631041310749:"『🛰』Н.А.-г.Лыткарино[Общий]", 751173868755877899:"『 🔓 』Кабинет Заместителя Директора СМИ", 751173926104596480:"『 🔓 』Кабинет Директора СМИ", 662731919968174097:"『📃』система-повышения", 813505363021267014:"『📃』антиблат-мз-а", 662732045650362379:"『📃』общение", 662731965539287071:"『📃』отчёты-на-повышение", 662731710110367794:"『🚑』Приёмная", 662731408820666409:"『💉』Больница г. Арзамас [Общий]", 662731578077610024:"『 🔓 』Кабинет Зам. Глав. Врача", 662731609925091338:"🧪┃Кабин  ет Глав. Врача", 662733302997975049:"『📃』система-повышения", 662733276045246474:"『📃』отчёты-на-повышение", 662733256604778563:"『📃』общение", 813505972663353374:"『📃』антиблат-мз-э", 662733035157979136:"『🚑』Приёмная", 662733095832780810:"『💉』Поликлиника г.Лыткарино [Общий]", 662733144880840744:"『 🔓 』Кабинет Зам. Глав. Врача", 662733182017208321:"『 🔓 』Кабинет Глав. Врача", 751174848495222934:"『📃』система-повышения", 751174641090953256:" отчёты-на-повышение", 751174954027974656:"『📃』общение", 813506228735049740:"『📃』антиблат-мз-л", 751175857774788751:"💉┃Приёмная", 751176517660311642:"💉┃Поликлиника г.Лыткарино [Общий]", 751179791318646874:"『 🔓 』Кабинет Зам. Глав. Врача", 751179830946693210:"『 🔓 』Кабинет Глав. Врача", 662373582059339797:"『🗡』Украинская Мафия", 662373619942555699:"『🔪』Русская Мафия", 662373761307115559:"『💀』Кавказкая Мафия", 662372330223435796:"『😈』Фантомасы", 662372388272603156:"『🕵』Санитары", 662372262921502745:"『🕴』Чёрные Кошки", 662372307616137217:"『🧛』Солнцевская Братва", 815949362798657616:"『🔔』Кандидаты", 615656412021915777:"『⛔』Обзвон ГОС", 815945367027187713:"『⛔』Обзвон НЕЛ", 615656470893297664:"『⏳』Ожидание итогов ГОС", 815945686678896690:"『⏳』Ожидание итогов НЕЛ", 840311954114347028:"『🧾』Кандидаты", 840312064403963935:"『⛔』Обзвон Админ", 840312025774030848:"『⏳』Ожидание итогов", 477875735416274954:"『💬』admins-chat", 477583783638335498:"『🧤』Общение Администрации.", 477583681570209792:"『🔔』Собрание Администрации.", 675074859935465472:"『👥』Приват [1]", 802874977924939786:"『👥』Приват [2]", 674597605552029706:"『👥』Приват [3]", 477879828859846656:"『🔞』Старшая Администрация.", 477549251619061770:"『💰 』Казнь", 637657062091784202:"『💾』Гл. Администрация", 720580370202099764:"『 🛡』Ожидание аттестации", 720360917556002827:"『🧣』Аттестация [2]", 745612580340367421:"『💎』Постановление хелперов", 826068286059184158:"『💎』Собрание", 477553310145052674:"『🌙』АФК", 833729786266386502:"『💤』голосовой-log", 833729787914485781:"『💤』каналы-log", 833729790024482886:"『💤』изменение-ролей-log", 833729792138281040:"『💤』сообщения-log", 833729793974730822:"『💤』добавление-ролей-log"}

    for i in ctx.guild.categories:
        for b in i.text_channels:
            try:
                await b.edit(name = jsp[b.id])
            except:
                pass
        for b in i.voice_channels:
            try:
                await b.edit(name = jsp[b.id])
            except:
                pass

@bot.command()
@commands.is_owner()
async def getruless(ctx): 
    await ctx.message.delete()
    e = discord.Embed(title = 'Основное положение | Северный Округ', description = '**1.1** При входе в Discord-сервер СО, вы соглашаетесь выполнять все перечисленные ниже правила.\n**1.2** Незнание правил не освобождает вас от ответственности за их нарушение.\n**1.3** Правила могут быть дополнены или изменены в любой момент, без оповещения и объяснения на то причины.\n**1.4** Изменения правил вступают в силу сразу после редактирования, без оповещения кого-либо.\n**1.5** В некоторых категориях/каналах некоторые правила могут не действовать.\n**1.6** Модерация сервера вправе плюсовать меру наказаний при грубых нарушениях, не злоупотребляя данной возможностью.\n**1.7** Многократные нарушения в течение дня/продолжительного времени дают модерации право выдать более серьезное наказание `(по согласованию с ГМ/ЗГМ)`.\n**1.8** Старший состав модерации дискорда имеет право выдавать наказания больше определённой нормы без объяснения на то причины.\n**1.9** Старший состав модерации в праве выбирать и сортировать контингент дискорд-сервера на своё личное усмотрение.', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Аккаунты Discord | Северный Округ', description = '**2.1** Запрещено создавать один и тот же аккаунт более `2-х` раз, при этом нарушая правила дискорд сервера на одном из них. `[Ban без возможности восстановления]`\n**2.2** Запрещено создавать фейковые аккаунты и использовать их одновременно с основными. `[Ban]`\n**2.3** Запрещено обходить систему наказаний перезаходом `(релогом)` на сервер или любыми другими методами. `[Ban 10d]`\n**2.4** Запрещено иметь оскорбительные/неадекватные статусы. `[Kick]`\n**2.5** Запрещено рекламировать что-либо в статусе аккаунта с целью «наживы» на участниках сервера. (Исключение: Индивидуальные ссылки одобренные модерацией) `[Ban 30d]`\n**2.6** Многократные нарушения правил дискорда в определённо-установленный на каждое из них, исходя их их весемости период времени, более `5-ти` раз `[От: Mute 30m | До: Ban permanent]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Никнеймы пользователей | Северный округ', description = '\n**3.1** Запрещено иметь специализированные теги `([A], [SP], [Х], [СЗМ] и т.д.)`, если вы не являетесь администратором/модератором. `[смена + Warn]`\n**3.2** Запрещено вводить в заблуждение участников, устанавливая чужие никнеймы `(включая ники игроков)`. `[смена + Warn, при повторе – Ban 10d]`\n**3.3** Запрещено устанавливать некнеймы людей, находящихся в черном проекте проекта/сервера. `[смена + Warn, при повторе – Ban 20d]`\n**3.4** Запрещено использовать оскорбительные/матерные никнеймы, включая Discord-тег. `[смена + Warn, при отказе – Ban 30d]`\n**3.5** Запрещено искажать в оскорбительной форме никнеймы  других участников. `[смена + Warn, при повторе – Ban 30d]`\n**3.6** Запрещено иметь оскорбительный никнейм либо косвенно указывать на оскорбление кого-либо в нике, либо завуалированно оскорблять кого-либо из участников дискорд-сервера. `[смена + Warn, при повторе – Ban 30d]`\n**3.7** Разрешено добавлять смайлы в никнейм`(Лимит: 3 emoji, 3 символа не относящихся к латинице/русскому или английскому алфавиту)`.\n**3.8** Ник не может состоять полностью из букв верхнего регистра `(Caps)` в случае если он состоит из 12+ символов. `[смена, при отказе – Warn]`\n**3.9** Формой для фракционного никнейма является: `[Фракция | Ранг/10] Nick_Name` | Пример: `[ФСБ | 7/10] Dollar_Baby` | При наличии нескольких тег-должностей, необходимо разделять их знаком **|**. `[Смена никнейма]`\n**3.10** Формой ников для администрации является: `[A | **args] Nick_Name`(**args – Аргументы`(теги)` для следящих, пример: `ГС Пра-во`) | Пример никнейма: `[A | ГС МВД] Dollar_Baby.` `[Смена никнейма + снятие админской роли]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Роли участников | Северный округ', description = '**4.1** Запрещено запрашивать фракционную роль, если вы не состоите в организации. `[Warn]`\n**4.2** Запрещено иметь более `2-х` семейных ролей. `[снятие роли, при повторе – Warn]`\n**4.3** Роль `«Хранитель»` выдается бывшим администраторам от 3-го уровня, администраторам `4-го` уровня и выше с других серверов.', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Аватарки и баннеры пользователей | Северный округ', description = '**5.1** Запрещено использование аватаров с эротичным содержанием/сценами насилия/межнационального деления(Исключение: `Аватары лично одобренные модерацией`) `[Ban 30d]`\n**5.2** Запрещено устанавливать аватарки/баннеры, пропагандирующие экстремистские организации, нацизм, фашизм, насилие, межрасовые конфликты, призывы к суициду. `[Warn / Ban]`\n**5.3** Запрещено устанавливать аватарки/баннеры, оскорбляющие/затрагивающие чувства кого-либо из участников сервера. `[Ban 30d]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Текстовые каналы | Северный округ', description = '**Общие правила чата**\n**6.1** Запрещено использовать мат, в том числе, завуалированный. `[mute 10-40m / на усмотрение модерации]`\n**6.2** Запрещено флудить/спамить (однотипные сообщения в количестве от 3-х и более). `[mute 40m]`\n**6.3** Запрещено оффтопить во фракционных/специализированных (запрос роли, проверка уровня, казино, музыка) каналах. `[mute 30m]`\n**6.4** Запрещено флудить символами/смайлами/стикерами. `[mute 40m]`\n**6.5** Запрещено участие в коллективном флуде. `[mute 120m]`\n**6.6** Запрещено накручивать ранг в Discord любым образом, в том числе, текстовым. `[Ban 5d]`\n**6.7** Запрещено злоупотреблять функцией «CapsLock». `[mute 30m]` `(наказание выдается по усмотрению модерации)`\n**6.8** Запрещено неадекватное поведение. `[mute 180m]`\n**6.9** Запрещено обсуждение политической деятельности в негативном ключе. `[Ban 10d]`\n**6.10** Запрещено оскорбление родных любым образом (текст, аватар, баннер, статус, тег). `[Ban]`\n**6.11** Запрещено распространение контента `18+` формата или эротического содержания, а так же сцен `нисилия/межнационального деления`, контента содержащего упоминание: `экстремистских организаций, нацизма, фашизма, насилия над кем-либо`, а так же содержащие направление на: `межрасовые конфликты`, и: `призывы к суициду`. `[mute 240m  /  Warn]`\n**6.12** Запрещено ставить большое количество реакций от одного участника на сообщения. `[mute 60m]`\n**6.13** Запрещено упоминать любые роли без весомой причины. `[mute  40m]`\n**6.14**  Лидерам/замам разрешается в разумных пределах флудить в своих фракционных каналах упоминанием роли для приглашения в игру.\n**6.15** Запрещено пиарить кандидатов на пост Губернатора. `[Ban 15d]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Текстовые каналы | Северный округ', description = '**Касаемо администрации/модерации:**\n 6.16 Запрещено неуважительное отношение к модерации/администрации. `[mute 30m]`\n**6.17** Запрещено завуалированное/прямое оскорбление администрации/модерации, том числе, отправка любых уничижительных заявлений в любой форме (текст, медиа). `[mute 180m + Warn по ситуации]`\n**6.18** Запрещено провоцирование администрации/ модерации на конфликт или выдачу наказаний. `[mute 120m]`\n**6.19** Запрещено публичное обсуждение действий администрации/модерации, в том числе, обсуждение наказаний, выданных в игре или в дискорд-сервере `[mute 120m]`\n**6.20** Запрещено выдавать себя за администрацию / модерацию. `[Ban 15d]`\n**6.21** Запрещен обман модерации, в том числе, при выдаче фракционных ролей, если вы не состоите в организации. `[mute 180m / Warn]`\n\n**Касаемо игроков:** \n**6.22** Запрещено разводить/поддерживать конфликты. `[mute 60m каждому участнику конфликта]`\n**6.24** Запрещено завуалированное/прямое оскорбление игроков. `[mute 80m]`\n**6.25** Запрещена завуалированная провокация и агрессия в сторону любого участника сервера. `[mute 80m]`\n**6.25** Запрещены прямые/косвенные угрозы любому участнику сервера. `[mute 80m]`\n**6.26** Запрещены попытки обмана, мошенничества игроков в корыстных целях. `[Warn]`\n\n**Отправляемые ссылки / медиа:**\n**6.27** Запрещено отправлять мемы больше 5 раз за 10 минут. `[mute 60m / Warn]`\n**6.28** Запрещена реклама любых групп, игр, YouTube-каналов, сайтов (исключение: `Rodina/Arizona/Жизнь В Деревне`). `[Ban 30d]`\n**6.29** Запрещена отправка медиа-контента, выставляющего в положительном свете национализм, фашизм, насилие, издевательства над людьми и животными. [Ban 10d]\n**6.30** Запрещена пропаганда суицида, экстремистских и террористических организаций. `[Ban 5d]`\n**6.31** Запрещена отправка медиа-контента, осуждающего/оскорбляющего любую национальность, вероисповедание, культуру и т.д. `[Ban 10d]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Голосовые каналы | Северный округ', description = '**7.1** Запрещено неадекватное поведение. `[mute 100m]`\n**7.2** Запрещено кричать в микрофон и создавать дополнительные шумы, мешая другим участникам. `[mute 60m]`\n**7.3** Запрещено транслировать музыку через микрофон. `[mute 80m]`\n**7.4** Запрещено использование программ для изменения голоса/создания звуковых эффектов. `[Ban 5d, при повторе + 5d]`\n**7.5** Запрещено разводить/поддерживать конфликты. `[mute 60m]`\n**7.6** Запрещено упоминание/оскорбление родных. `[Ban]`\n**7.7** Запрещено публичное осуждение действий администрации/модерации. `[mute 60m]`\n**7.8** Запрещено неуважительное отношение к администрации/модерации. `[mute 120m]`\n**7.9** Запрещено размучивать участника без договоренности с модерацией, если ему было выдано наказание (касается игроков, имеющих право доступа к отключению микро других). `[Warn]`\n**7.1**0 Запрещено обсуждение политической деятельности в негативном ключе. `[mute 30m]`\n**7.1**1 Запрещена трансляция любых групп, игр, YouTube-каналов, сайтов в рекламных целях (исключение: `Rodina/Arizona/Жизнь В Деревне`). `[Ban 30d]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)
    e = discord.Embed(title = 'Использование музыкальных ботов | Северный округ', description = '**8.1** Для получения роли Диджея `(10 семечек)` или VIP-Диджея `(15 семечек)` нужно получить соответствующее количество валюты Discord-сервера North District и оформить покупку в канале <#805487247692005417>\n**8.2** Запросы композиций Музыкальному боту можно писать исключительно в музыкальном канале. `[mute 60m, при повторе – Снятие роли Музыканта]`\n**8.3** Запрещено во время проигрывания композиции специально кричать, издавать звуки, не относящиеся к песне. `[mute 120m]`\n**8.4** Запрещается пропускать чужие композиции без причины. `[отключение от канала, при повторе – Warn]`\n**8.5** Запрещено включать композиции с неадекватным/откровенным содержанием. `[mute 180m, при повторе – Warn]`\n**8.6** Добавление и прослушивание музыки в каналах фракций разрешено исключительно в нерабочее время. `[mute 60m, при повторе – Снятие роли Музыканта]`', colour = 0xFB9E14)
    e.set_footer(text = f'Support Team by dollar ム baby#3603 & lalalalal#1125', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    e.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed = e)


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author

    user = ctx.message.author if (member == None) else member
    embed = discord.Embed( description = f'''{author.mention}, вот аватар пользователя {user.mention}:''', color= 0xFB9E14)
    embed.set_image(url=user.avatar_url_as(format = None, size = 4096))
    embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    embed.set_thumbnail(url = ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator = True)
async def allsn(ctx, member: discord.Member):
    number = 0
    mas = [ ]
    for i in rolef.find({"is_active": 2, "leader": member.id}):
        channel = bot.get_channel(i["kuda"])
        message = await channel.fetch_message(i["message_id"])
        await message.delete()
        rol = ctx.guild.get_role(i["role_id"])
        chan = bot.get_channel(i["channel"])
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

@buttons.click
async def button_stats_r(ctx):
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')

    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member
    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    member = ctx.guild.get_member(rolecheck["user_id"])  
    chan = bot.get_channel(rolecheck["channel"])
    if rolecheck["pruf"] == 0:
        await chan.send(f'{member.mention}, `модератор` {memb.mention} `запрашивает у вас статистику игрового аккаунта, отправьте в личные сообщения боту скриншот [/stats + /time]`')
        serf = await channel.send(f'`[PRUF]` {memb.mention} `запросил доказательства от {member.display_name}, c ID: {rolecheck["user_id"]}`')
        rolef.update_one({"message_id": message.id}, {"$set": {"pruf": 1, "zaproschannel": channel.id, "zapid": serf.id}})
        await member.send(f'{member.mention}, `модератор {memb.display_name} запрашивает у вас статистику игрового аккаунта, отправьте в личные сообщения боту скриншот [/stats + /time]`')
    else:
        await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Ошибочка__**', description = 'Статистику уже запросил другой модератор.'), flags = MessageFlags().EPHEMERAL)

@buttons.click
async def button_lider_r(ctx):
    global role_checkers
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member
    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    member = ctx.guild.get_member(rolecheck["user_id"])  
    chan = bot.get_channel(rolecheck["channel"])
    for role in member.roles:
        if role.id in role_checkers:
            await member.remove_roles(role)
        else:
            pass

    if not rolecheck["prufid"] == 0:
        msg = await channel.fetch_message(rolecheck["prufid"])
        await msg.delete()

    if not rolecheck["zapid"] == 0:
        msg1 = await channel.fetch_message(rolecheck["zapid"])
        await msg1.delete()
        
    role = ctx.guild.get_role(rolecheck["role_id"])
    await member.add_roles(role)
    await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу роли.`\n`Роль ({role.name}) была выдана!`')
    await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от {member.display_name}, c ID: {rolecheck["user_id"]}`')
    rolef.delete_one({"message_id": message.id})
    add(memb, "rols")
    await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Юхууу, новое действие__**', description = f'Вы одобрили выдачу роли {role.mention} пользователю {member.mention}`({member})`\n\n**Действие добавлено в вашу модерскую статистику** `(!imd)`.'), flags = MessageFlags().EPHEMERAL)
    return await message.delete()

@buttons.click
async def button_deny_r(ctx):
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member
    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    if rolecheck["is_active"] == 1:
        member = ctx.guild.get_member(rolecheck["user_id"])  
        chan = bot.get_channel(rolecheck["channel"])
        if not rolecheck["prufid"] == 0:
            msg = await channel.fetch_message(rolecheck["prufid"])
            await msg.delete()

        if not rolecheck["zapid"] == 0:
            msg1 = await channel.fetch_message(rolecheck["zapid"])
            await msg1.delete()

        await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на выдачу роли.`\n`Ваш ник при отправке: {member.display_name}`\n`Установите ник на: [Фракция Ранг/10] Имя_Фамилия`')
        await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {rolecheck["user_id"]}`')
        rolef.delete_one({"message_id": message.id})
        await message.delete()
        await ctx.reply(embed = discord.Embed(title = '\⛩️ **__У вас получилось__**', description = f'Вы удалили запрос на выдачу роли пользователю {member.mention}`({member})`'), flags = MessageFlags().EPHEMERAL)

@buttons.click
async def button_deny_s(ctx):
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member
    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    if rolecheck["is_active"] == 2:
        chan = bot.get_channel(rolecheck["channel"])
        member = ctx.guild.get_member(rolecheck["leader"])
        if member.id == memb.id:
            await channel.send(f'`[DENY]` {memb.mention} `удалил свой запрос`')
        else:
            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на снятие роли у пользователя` <@!{rolecheck["user_id"]}>`.`')
            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {rolecheck["user_id"]}`')
        rolef.delete_one({"message_id": message.id})
        await message.delete()
        await ctx.reply(embed = discord.Embed(title = '\⛩️ **__У вас получилось__**', description = f'Вы удалили запрос на выдачу роли пользователю {memb.mention}`({memb})`'), flags = MessageFlags().EPHEMERAL)

@buttons.click
async def button_remove_r(ctx):
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member
    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    if rolecheck["is_active"] == 1:
        member = ctx.guild.get_member(rolecheck["user_id"])  
        chan = bot.get_channel(rolecheck["channel"])
        await message.delete()
        if not rolecheck["prufid"] == 0:
            msg = await channel.fetch_message(rolecheck["prufid"])
            await msg.delete()

        if not rolecheck["zapid"] == 0:
            msg1 = await channel.fetch_message(rolecheck["zapid"])
            await msg1.delete()

        await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на выдачу роли.`\n`Ваш ник при отправке: {member.display_name}`\n`Установите ник на: [Фракция Ранг/10] Имя_Фамилия`')
        await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {rolecheck["user_id"]}`')
        rolef.delete_one({"message_id": message.id})
        await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Юхууу, почти новое действие__**', description = f'Вы отклонили выдачу роли пользователю {member.mention}`({member})`\n\n**Данное действие пока что не добавляется в вашу модерскую статистику** `(!imd)`.'), flags = MessageFlags().EPHEMERAL)

@buttons.click
async def button_remove_s(ctx):
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member

    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    if rolecheck["is_active"] == 2:
        member = ctx.guild.get_member(rolecheck["user_id"])  
        chan = bot.get_channel(rolecheck["channel"])

        member = ctx.guild.get_member(rolecheck["leader"])
        await message.delete()
        await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на снятие роли у пользователя` {member.mention}')
        await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {rolecheck["user_id"]}`')
        rolef.delete_one({"message_id": message.id})
        await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Юхууу, почти новое действие__**', description = f'Вы отклонили снятие роли пользователю {member.mention}`({member})`\n\n**Данное действие пока что не добавляется в вашу модерскую статистику** `(!imd)`.'), flags = MessageFlags().EPHEMERAL)

@buttons.click
async def button_accept_r(ctx):
    global role_checkers
    
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member

    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    if rolecheck["is_active"] == 1:              
        member = ctx.guild.get_member(rolecheck["user_id"])  
        chan = bot.get_channel(rolecheck["channel"])
        for role in member.roles:
            if role.id in role_checkers:
                await member.remove_roles(role)
            else:
                pass

        if not rolecheck["prufid"] == 0:
            msg = await channel.fetch_message(rolecheck["prufid"])
            await msg.delete()

        if not rolecheck["zapid"] == 0:
            msg1 = await channel.fetch_message(rolecheck["zapid"])
            await msg1.delete()
        
        if rolecheck["leader"] > 1:
            role, role2 = ctx.guild.get_role(rolecheck["role_id"]), ctx.guild.get_role(rolecheck["leader"])
            await member.add_roles(ctx.guild.get_role(rolecheck["role_id"]))
            await member.add_roles(ctx.guild.get_role(rolecheck["leader"]))
            await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу фракционных ролей.`\n`Роли ({role.name}) и ({role2.name}) были выданы!`')
            await ctx.message.delete()
            await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Юхууу, новое действие__**', description = f'Вы одобрили выдачу ролей {role.mention} и {role2.mention} пользователю {member.mention}`({member})`\n\n**Действие добавлено в вашу модерскую статистику** `(!imd)`.'), flags = MessageFlags().EPHEMERAL)
        else:
            role = ctx.guild.get_role(rolecheck["role_id"])
            await member.add_roles(ctx.guild.get_role(rolecheck["role_id"]))
            await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу роли.`\n`Роль ({role.name}) была выдана!`')
            await ctx.message.delete()
            await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Юхууу, новое действие__**', description = f'Вы одобрили выдачу роли {role.mention} пользователю {member.mention}`({member})`\n\n**Действие добавлено в вашу модерскую статистику** `(!imd)`.'), flags = MessageFlags().EPHEMERAL)
        await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от {member.display_name}, c ID: {rolecheck["user_id"]}`')
        rolef.delete_one({"message_id": message.id})
        add(memb, "rols")

@buttons.click
async def button_accept_s(ctx):
    if rolef.count_documents({"message_id": ctx.message.id}) == 0: 
        await ctx.message.delete()
        return await ctx.channel.send(f'`[BUGTRAKER]` {ctx.member.mention} `удалил багнутый запрос`')
    if not ctx.channel.id == 505009452571820032: return
    if ctx.guild == None: return
    if not ctx.guild.id == 477547500232769536: return
    if ctx.member.bot: return
    channel = ctx.channel
    message = ctx.message
    memb = ctx.member

    rolecheck = rolef.find_one({"message_id": ctx.message.id})
    if rolecheck["is_active"] == 2:
        member = ctx.guild.get_member(rolecheck["user_id"])  
        chan = bot.get_channel(rolecheck["channel"])
        membs = ctx.guild.get_member(rolecheck["leader"])
        if membs.id == memb.id:
            return

        await message.delete()
        rol = ctx.guild.get_role(rolecheck["role_id"])
        await chan.send(f'`[ACCEPT]` {memb.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {member.display_name}, с ID: {member.id}`')
        await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {member.display_name}, с ID: {member.id}`')
        await member.remove_roles(rol)
        rolef.delete_one({"message_id": message.id})
        add(memb, "derols")
        await ctx.reply(embed = discord.Embed(title = '\⛩️ **__Юхууу, новое действие__**', description = f'Вы одобрили снятие роли пользователю {rol.mention} пользователю {member.mention}`({member})`\n\n**Действие добавлено в вашу модерскую статистику** `(!imd)`.'), flags = MessageFlags().EPHEMERAL)
            
@bot.event
async def on_message(ctx):
    global ROLES
    global gos
    global opg
    global nick_registr
    if ctx.content == f'<@!{bot.user.id}>' or  ctx.content == f'<@{bot.user.id}>':
        #await ctx.channel.send(f'{ctx.author.mention},', embed = discord.Embed(title = 'Основная информация', description = f'**Привет! Меня зовут Rodina RP бот.\nСоздатель бота: adminhelper#777\n\n> `Префикс установленный на этом сервере:`    /\n> `Ссылка на добавление бота:` https://discord.com/api/oauth2/authorize?client_id=729309765431328799&permissions=8&scope=bot\n\n`Информация о боте -` /botinfo\n`Информация по командам -` /help**', colour = 0xFB9E14), delete_after = 20)
        return

    global uje
    role_registr = ['!роль', 'роль', 'Роль', '!Роль']

    if not ctx.author.bot:
        if not ctx.guild:
            for i in rolef.find({"user_id": ctx.author.id}):
                if not i["zaproschannel"] == 0:
                    if ctx.attachments == []:
                        return
                    else:
                        chanel = bot.get_channel(i["zaproschannel"])
                        guild = bot.get_guild(477547500232769536)
                        member = discord.utils.get(guild.members, id = i["user_id"])
                        message = await bot.get_channel(i["zaproschannel"]).fetch_message(i["message_id"])
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
                        embed.add_field(name = 'Отправлено с канала', value = f'{bot.get_channel(i["zaproschannel"]).mention}', inline = False)
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
                      
        elif ctx.guild.id != 477547500232769536 and ctx.guild.id != 577511138032484360: return 
        
    await bot.process_commands(ctx)        
    msg = ctx.content.lower()
    if not ctx.guild.id == 477547500232769536: return
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
            msg2 = await bot.wait_for('message', timeout = 30.0, check = checkms)
        except Exception:
            await msg1.delete()
            return
        await msg1.delete()
        reas = msg2.content
        await msg2.delete()

        channel, nad_role = bot.get_channel(505009452571820032), discord.utils.get(ctx.guild.roles, id=z)
        
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
        await buttons.send(embed = embed, channel = channel.id, components = [ActionRow([Button(emoji = {"id": None,"name": "✔️","animated": False}, style = ButtonType().Success, custom_id = "button_accept_s"), Button(emoji = {"id": None,"name": "❌","animated": False}, style = ButtonType().Danger, custom_id = "button_remove_s"), Button(emoji = {"id": None,"name": "🇩","animated": False}, style = ButtonType().Primary, custom_id = "button_deny_s")])])
        await asyncio.sleep(0.5)
        message = channel.last_message
        rolef.insert_one({"user_id": member.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 2, "channel": ctx.channel.id, "leader": ctx.author.id, "kuda": channel.id})

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
            
            embed = discord.Embed(title = 'Получение ролей', description = f'**В Вашем ник-нэйме указан неверный тэг!\n`Discord >> Список всех фракционных тэгов`**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
            embed.add_field(name = f'**Тэги Государственных Организаций:**', value = f'> `Пра-во, Банк, МРЭО, ФСБ, ГИБДД, ГУВД, РОВД, Армия, ТСР, НГ-А, НГ-Л, МЗ-А, МЗ-Э, МЗ-Л, Судья`')
            embed.add_field(name = f'**Дополнительные тэги Нелегальных Организаций**', value = f'> `ФМ, СТ, СБ, ЧК, КМ, РМ, УМ`')
            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            embed.set_thumbnail(url = ctx.guild.icon_url)
            await ctx.channel.send(embed = embed, delete_after = 25)
            await asyncio.sleep(60)

        if z in nick_registr:
            if rolef.count_documents({"user_id": ctx.author.id}) == 1 and rolef.find_one({"user_id": ctx.author.id})["is_active"] == 1:
                await ctx.add_reaction('🕐')
                return await ctx.channel.send(f'{ctx.author.mention}, `Вы уже отправили своё заявление на получение роли, дождитесь его одобрения.`', delete_after = 5)

            channel = bot.get_channel(505009452571820032)
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
                embed.add_field(name = 'Действия', value = '`[✔️] - выдать роли старшего состава и организации.`\n`[➕] - Выдать роль организации`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`\n`[❔] - Запросить скрин-шот статистики`')
            else:
                embed.add_field(name = 'Действия', value = '`[✔️] - выдать роль.`\n`[❌] - отказать.`\n`[🇩] - удалить сообщение.`\n`[❔] - Запросить скрин-шот статистики`')
            embed.set_image(url = ctx.author.avatar_url)

            if nad_role in ctx.author.roles:
                await ctx.channel.send(f'{ctx.author.mention}, `у вас уже есть роль` {nad_role.mention}', delete_after = 5)
                return await ctx.add_reaction('❌')

            if not lidrole == 1:
                await buttons.send(embed = embed, channel = channel.id, components = [ActionRow([Button(emoji = {"id": None,"name": "✔️","animated": False}, style = ButtonType().Success, custom_id = "button_accept_r"), Button(emoji = {"id": None,"name": "➕","animated": False}, style = ButtonType().Success, custom_id = "button_lider_r"), Button(emoji = {"id": None,"name": "❌","animated": False}, style = ButtonType().Danger, custom_id = "button_remove_r"), Button(emoji = {"id": None,"name": "🇩","animated": False}, style = ButtonType().Primary, custom_id = "button_deny_r"), Button(emoji = {"id": None,"name": "❔","animated": False}, style = ButtonType().Success, custom_id = "button_stats_r")])])
                await asyncio.sleep(0.5)
                message = channel.last_message
                rolef.insert_one({"user_id": ctx.author.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 1, "channel": ctx.channel.id, "leader": lidrole.id, "pruf": 0, "zaproschannel": 0, "prufid": 0, "zapid": 0, "kuda": channel.id, "setn": 0})
            else:
                await buttons.send(embed = embed, channel = channel.id, components = [ActionRow([Button(emoji = {"id": None,"name": "✔️","animated": False}, style = ButtonType().Success, custom_id = "button_accept_r"), Button(emoji = {"id": None,"name": "❌","animated": False}, style = ButtonType().Danger, custom_id = "button_remove_r"), Button(emoji = {"id": None,"name": "🇩","animated": False}, style = ButtonType().Primary, custom_id = "button_deny_r"), Button(emoji = {"id": None,"name": "❔","animated": False}, style = ButtonType().Success, custom_id = "button_stats_r"), ])])
                await asyncio.sleep(0.5)
                message = channel.last_message
                rolef.insert_one({"user_id": ctx.author.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 1, "channel": ctx.channel.id, "leader": 0, "pruf": 0, "zaproschannel": 0, "prufid": 0, "zapid": 0, "kuda": channel.id, "setn": 0})
            
            await ctx.add_reaction('📨')

'''
#global stavka
#stavka = []

#global f
#f = 0

@bot.command()
async def ставка(ctx, storona = None):
    global f
    global stavka

    if f >= 20:
        await ctx.send('`[ERR] Ставки не принимаются`.')
        return

    if storona == None:
        await ctx.send('`[ERR] Укажите сторону за которую хотите проголосовать.`\n> `Светлая` - Мирные жители, врач, шериф\n> `Тёмная` - Мафия, Дон мафии.')
        return
        
    if f'{ctx.author.id} | {ctx.author.display_name} `| Тёмная`\n' in stavka or f'{ctx.author.id} | {ctx.author.display_name} `| Светлая`\n' in stavka:
        await ctx.send('`[ERR] Вы уже сделали свою ставку`.')
        return

    if storona == 'Светлая':
        f += 1
        await ctx.send(f'`[ACCEPT]` {ctx.author.mention}, `вы успешно проголосовали за светлую сторону!`')
        stavka.append(f'{ctx.author.id} | {ctx.author.display_name} `| Светлая`\n')
        member = discord.utils.get(ctx.guild.members, id=646573856785694721)
        await member.send(embed = discord.Embed(description = f'**Пользователь {ctx.author.display_name} | ID: {ctx.author.id} сделал ставку на `Светлую` сторону.**'))

    elif storona == 'Тёмная':
        f += 1
        await ctx.send(f'`[ACCEPT]` {ctx.author.mention}, `вы успешно проголосовали за тёмную сторону!`')
        stavka.append(f'{ctx.author.id} | {ctx.author.display_name} `| Тёмная`\n')
        member = discord.utils.get(ctx.guild.members, id=646573856785694721)
        await member.send(embed = discord.Embed(description = f'**Пользователь {ctx.author.display_name} | ID: {ctx.author.id} сделал ставку на `Тёмную` сторону.**'))

    else:
        await ctx.send('`[ERR] Укажите сторону за которую хотите проголосовать.`\n> `Светлая` - Мирные жители, врач, шериф\n> `Тёмная` - Мафия, Дон мафии.')

    if f == 20:
        str_a = ''.join(stavka)
        member = discord.utils.get(ctx.guild.members, id=646573856785694721)
        await member.send(embed = discord.Embed(description = f'**Пользователи сделавшие ставки:\n{str_a}**'))
'''
bot.run('NzI5MzA5NzY1NDMxMzI4Nzk5.XwHEpQ.eC2EUwcEblO_HaoX5gCinF27XI8')
