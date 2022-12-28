import discord
import asyncio
from discord.ext import commands
from random import randint

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents= intent)

users = {}

item = {'nomal' : ['낡은 단검', '하급 회복 포션'], 'rare' : ['중급 회복 포션']}

stage = {
    "green_forest" : {
        'stage_count' : 3,
        'stage' : [{
            'stage' : 1,
            'monster' : {
                'name' : "슬라임",
                'hp' : 3,
                'atk' : 1,
                'def' : 0,
                'xp' : 1,
                'money' : 10
            }},{
            'stage' : 2,
            'monster' : {
                'name' : "슬라임",
                'hp' : 3,
                'atk' : 1,
                'def' : 0,
                'xp' : 1,
                'money' : 10
            }},{
            'stage' : 3,
            'monster' : {
                'name' : "대왕 슬라임",
                'hp' : 5,
                'atk' : 1.5,
                'def' : 0,
                'xp' : 3,
                'money' : 30
            }}]
            }
}


@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)    
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)
    
@bot.command()
async def 계정생성(ctx):
    id = ctx.message.author.id
    name = ctx.message.author.name
    if id in users.keys():
        await sendff(ctx, "계정 생성 오류", "계정이 이미 존제 합니다.", "red")
    else:
        users[id] = {'name' : name, 
                    'money' : 100,
                    'atk' : 1,
                    'hp_max' : 7,
                    'hp' : 7,
                    'def' : 1,
                    'lv' : 1,
                    'xp' : 0,
                    'xp_max' : 4,
                    'item' : {'test1':1,'test2':2}}
        await sendff(ctx, "계정 생성 성공", f"이름 : {users[id]['name']}\n소지금 : {users[id]['money']}g\n채력 : {users[id]['hp']}/{users[id]['hp_max']}\n공격력 : {users[id]['atk']}\n방어력 : {users[id]['def']}\nLv : {users[id]['lv']}\nXp : {users[id]['xp']}/{users[id]['xp_max']}","green")

@bot.command()
async def 정보(ctx):
    id = ctx.message.author.id
    if id in users.keys():
        await sendff(ctx, "정보", f"이름 : {users[id]['name']}\n소지금 : {users[id]['money']}g\n채력 : {users[id]['hp']}/{users[id]['hp_max']}\n공격력 : {users[id]['atk']}\n방어력 : {users[id]['def']}\nLv : {users[id]['lv']}\nXp : {users[id]['xp']}/{users[id]['xp_max']}","green")
        stri = f""
        for i in users[id]['item'].keys():
            stri = f"{stri}{i} X {users[id]['item'][i]}\n"
        await sendff(ctx, "가방", stri,'green')
    else:
        await sendff(ctx, "계정 오류", "계정이 존제하지 않습니다.", "red")

@bot.command()
async def 모험(ctx, *, stage):
    id = ctx.message.author.id
    if id in users.keys():
        if stage == "푸른숲":
            await trip_green_forest(ctx)
    else:
        await sendff(ctx, "계정 오류", "계정이 존제하지 않습니다.", "red")

async def trip_green_forest(ctx):
    name = ctx.message.author.name
    stage = 1
    global msg_trip
    global id_trip
    id_trip = ctx.message.author.id
    id = ctx.message.author.id
    msg_trip = await sendff(ctx,"진입중",f"{name}(은)는 푸른 숲으로 들어갔다...",'blue')
    #while stage <= stage['grean_forest']['stage_count'] and user[id]['hp'] > 0:
    await asyncio.sleep(2)
    await msg_trip.edit(embed = discord.Embed(title='모험중',description = f"{name}(은)는 푸른숲을 모험 중이다...", color = 0x0000ff))
    await asyncio.sleep(2)
    await trip_switch(ctx)

async def trip_switch(ctx):
    global stage_item
    stage_item = select_treasure(1)
    global trip_stage
    trip_stage = True
    await encounter_treasure(ctx)

def select_treasure(n):
    if n == 1:
        a = item['nomal'][randint(0, len(item['nomal'])-1)]
        return a


async def encounter_treasure(ctx):
    await msg_trip.edit(embed = discord.Embed(title='찾았다!!',description = f"{users[id_trip]['name']}(은)는 보물상자를 발견하였다.\n\n줍는다 | | \U0001F4B0\n버린다 | | \U0001F6AB", color = 0x00ff00))
    await msg_trip.add_reaction("\U0001F4B0")
    await msg_trip.add_reaction("\U0001F6AB")
    
@bot.event    
async def on_reaction_add(reaction, user):
    if trip_stage:
        if user.bot == 1: #봇이면 패스
            return None
        if str(reaction.emoji) == "\U0001F4B0":  
            await msg_trip.clear_reaction("\U0001F6AB")
            if stage_item in users[id_trip]['item'].keys():
                for i in users[id_trip]['item'].keys():
                    if i == stage_item:
                        users[id_trip]['item'][i] += 1
            else:
                users[id_trip]['item'][stage_item] = 1
            await msg_trip.edit(embed = discord.Embed(title='찾았다!!',description = f"{users[id_trip]['name']}(은)는 {stage_item}(을)를 획득 하였다.\n\n줍는다 | | \U0001F4B0", color = 0x00ff00))    
        if str(reaction.emoji) == "\U0001F6AB":
            await msg_trip.clear_reaction("\U0001F4B0")
            await msg_trip.edit(embed = discord.Embed(title='버렸다', description=f"{users[id_trip]['name']}(은)는 보물상자를 버렸다."))
async def sendff(ctx, titlef, descriptionf, colorf):
    if (colorf == "red"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0xff0000))
    elif (colorf == "green"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x00ff00))
    elif (colorf == "blue"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x0000ff))


async def sendf(ctx, msg):
    return await ctx.send(msg)

bot.run('MTA1NDIwNDI1Nzk2NTk3MzU2NQ.GvEZMs.D-4bI90UqETtLiWEgS5U-25-mqYDsk4TOM8p74') #test_dojin