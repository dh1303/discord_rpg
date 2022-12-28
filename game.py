import discord
import asyncio
from discord.ext import commands
from random import randint

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents= intent)

class player:
    def __init__(self, id,name,ctx,msg,do_play) -> None:
        self.id = id
        self.name = name
        self.ctx = ctx
        self.msg = msg
        self.do_play = do_play
        pass

message_id_list = {}

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)    
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

start_stats = {'money' : 100,
            'atk' : 1,
            'hp_max' : 7,
            'hp' : 7,
            'def' : 1,
            'lv' : 1,
            'xp' : 0,
            'xp_max' : 4,}



item = {'test1': {'grade' : 'nomal', 'price' : 15, 'name' : 'test1'},'test2' : {'grade' : 'rare', 'price' : 50, 'name' : 'test2'}}

shop_item_list = [item["test1"],item["test2"]]

users = {}
_player = {}

@bot.command()
async def test(ctx):
    id = ctx.message.author.id
    print("\n[start] test |",id,"\n")
    await creat_id(ctx)
    print("\n[end] test |", id,_player[id].name,_player[id].do_play,"\n")

@bot.command()
async def shop(ctx):
    id = ctx.message.author.id
    print("\n[start] shop |",id,"\n")
    await show_shop(ctx)
    print("\n[end] shop |", id,_player[id].name,_player[id].do_play,"\n")
    
@bot.command()
async def inventory(ctx):
    id = ctx.message.author.id
    print("\n[start] inventory |",id,"\n")
    await show_inventory(ctx)
    print("\n[end] inventory |", id,_player[id].name,_player[id].do_play,"\n")

@bot.command()
async def me(ctx):
    id = ctx.message.author.id
    print("\n[start] me |",id,"\n")
    await show_me(ctx)
    print("\n[end] me |", id,_player[id].name,_player[id].do_play,"\n")

@bot.command()
async def test1(ctx, *, item):
    id = ctx.message.author.id
    print("\n[start] test1 |",id,"\n")
    await add_item(ctx, item)
    print("\n[end] shop_buy |", id,_player[id].name,_player[id].do_play,"\n")
@bot.command()
async def help(ctx):
    await sendff(ctx, "명령어 정보","""
    help
    명령어의 정보를 알려준다.
    ===================================
    me
    내 정보를 알려준다.
    ===================================
    inventory
    내 가방을 연다.
    ===================================
    shop
    상점을 연다""", 'green')

@bot.event    
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        print("bot reaction!")
        return None
    id = user.id
    msg_id = reaction.message.id
    check_id(id)
    print("user reaction | msg_id :",msg_id,"user_id : ",id)
    print(message_id_list)
    if id == message_id_list[msg_id]:
        if _player[id].do_play == "creat_id":
            if str(reaction.emoji) == "\U0001F392":
                await show_inventory(_player[id].ctx)
                _player[id].do_play = None
                _player[id].msg = None
        if _player[id].do_play == "add_item":
            if str(reaction.emoji) == "\U0001F392":
                await show_inventory(_player[id].ctx)
                _player[id].do_play = None
                _player[id].msg = None
        if _player[id].do_play == "show_me":
            if str(reaction.emoji) == "\U0001F392":
                await show_inventory(_player[id].ctx)
                _player[id].do_play = None
                _player[id].msg = None
        if _player[id].do_play == "show_shop":
            if str(reaction.emoji) == "🫳": #구매
                print('buy')
                await shop_buy(_player[id].ctx)
                await _player[id].msg.clear_reaction("🫳")
            if str(reaction.emoji) == "🫴": #판매
                print('sell')
                await _player[id].msg.clear_reaction("🫴")
                await _player[id].msg.add_reaction("🫴")
            if str(reaction.emoji) == "🚫": #거래중단
                print('stop')
                _player[id].do_play = None
                _player[id].msg = None


async def shop_buy(ctx):
    id = ctx.message.author.id
    print("\n[start] shop_buy |", id,_player[id].name,_player[id].do_play,"\n")
    _player[id].ctx = ctx
    timeout = 20 # 기다릴 시간 정하기
    wait_msg = await sendff(ctx,"",f'구매하실 물품에 번호나 이름을 입력해 주세요', 'blue')
    message_id_list[wait_msg.id] = id
    await wait_msg.add_reaction("🚫")

    def check(m): # check 메서드 정의
        return m.author == ctx.message.author and m.channel == ctx.message.channel # 같은 채널에서 같은 메시지를 보낸 사람의 이벤트를 체크

    try: # 5초간 기다림
    	# 이벤트 입력 시 앞의 'on_'은 떼고 입력함
        msg = await bot.wait_for('message', check=check, timeout=timeout)
    except asyncio.TimeoutError: # 5초가 지나면 TimeoutError 발생
        await wait_msg.edit(embed = discord.Embed(title= "", description = '시간초과 입니다. \n다시 구매하기 : \"🫳\"\n취소 : \"🚫\"', color = 0xff0000))
        await wait_msg.add_reaction("🫳")
        print("\n[end] shop_buy |", id,_player[id].name,_player[id].do_play,"\n")
        return
    else: # 5초 안에 'on_message' 이벤트 수신 시
        try:
            print(1)
            buy_item = shop_item_list[int(msg.content) - 1]
            
        except:
            try:
                print(2)
                buy_item = item[msg.content]
                
            except:
                await wait_msg.edit(embed = discord.Embed(title= "", description = '존재하지 않는 아이탬입니다. \n다시 구매하기 : \"🫳\"\n취소 : \"🚫\"', color = 0xff0000))
                await wait_msg.add_reaction("🫳")
                print("\n[end] shop_buy |", id,_player[id].name,_player[id].do_play,"\n")
                return
        if buy_item['price'] <= users[id]['money']:
            print(users[id]['money'], buy_item['price'])
            users[id]['money'] -= buy_item['price']
            await add_item(ctx, buy_item['name'])
            await wait_msg.add_reaction("🫳")
        else:
            
            print("\n[end] shop_buy |", id,_player[id].name,_player[id].do_play,"\n")

async def add_item(ctx, item_name):
    id = ctx.message.author.id
    if ctx.message.author.id in users.keys():
        print("\n[start] add_item |", id,_player[id].name,_player[id].do_play,"\n")
        _player[id].ctx = ctx
        if item_name in item.keys():
            check_id(id)
            if item_name in users[id]['item'].keys():
                users[id]['item'][item_name] += 1
            else:
                users[id]['item'][item_name] = 1
            _player[id].msg = await sendff(_player[id].ctx,'아이탬 획득', f"{users[id]['name']}(이)가 {item_name}(을)를 획득하였습니다.",'green')
            message_id_list[_player[id].msg.id] = id
            _player[id].do_play = 'add_item'
            await _player[id].msg.add_reaction("\U0001F392")
            print("add_item :",item_name)
            print(users[id]['name'],":",users[id]['item'])
        else:
            await sendff(_player[id]['ctx'],'아이탬 획득 실패', f"{item_name}이란 아이탬이 존재하지 않습니다.",'red')
    else:
        print("\n[start] add_item |", id,"\n")
        await creat_id(ctx)
        await _player[ctx.message.author.id].msg.clear_reaction("\U0001F392")
        await add_item(ctx, item_name)
    print("\n[end] add_item |", id,_player[id].name,_player[id].do_play,"\n")

async def show_shop(ctx):
    id = ctx.message.author.id
    print("\n[start] show_shop |", id,"\n")
    if ctx.message.author.id in users.keys():
        print("\n[start] show_shop |", id,_player[id].name,_player[id].do_play,"\n")
        _player[id].ctx = ctx
        result = f"소지금 : {users[id]['money']}gold\n\n"
        count = 1
        for i in shop_item_list:
            result = f"{result}{count}. {i['name']}({i['grade']}) : {i['price']}gold\n"
            count += 1
        _player[id].msg = await sendff(ctx, "상점", f"{result}\n\n구매 : \"🫳\"\n판매 : \"🫴\"\n취소 : \"🚫\"", 'green')
        message_id_list[_player[id].msg.id] = id
        await _player[id].msg.add_reaction('🫳')
        await _player[id].msg.add_reaction('🫴')
        await _player[id].msg.add_reaction('🚫')
        _player[id].do_play = 'show_shop'

    else:
        await creat_id(ctx)
        await show_shop(ctx)
    print("\n[end] show_shop |", id,_player[id].name,_player[id].do_play,"\n")

async def creat_id(ctx):
    id = ctx.message.author.id
    print("\n[start] creat_id |", id,"\n")
    name = ctx.message.author.name
    if id in users.keys():
        await sendff(ctx, "계정 생성 실패", f"{name}님의 계정이 이미 존제합니다.", "red")
        print("\n[end] creat_id |", id,_player[id].name,_player[id].do_play,"\n")
    else:
        users[id] = {}
        users[id]['name'] = name
        for i in start_stats:
            users[id][i] = start_stats[i]
        result = f"""name : {users[id]['name']}
money : {users[id]['money']}gold
atk : {users[id]['atk']}
hp : {users[id]['hp']}/{users[id]['hp_max']}
def : {users[id]['def']}
lv : {users[id]['lv']}
xp : {users[id]['xp']}/{users[id]['xp_max']}"""
        result = f"{result}\n가방을 확인하려면\"\U0001F392\"을 클릭하세요!"
        users[id]['item'] = {}
        print("id :",id)
        message = await sendff(ctx, "계정 생성 성공", result, "green")
        await message.add_reaction("\U0001F392")
        print("message_id : ",message.id)
        message_id_list[message.id] = id
        _player[id] = player(id=id,name=name,ctx=ctx,do_play="creat_id",msg=message)
        print("\n[end] creat_id |", id,_player[id].name,_player[id].do_play,"\n")

async def show_inventory(ctx):
    id = ctx.message.author.id
    print("\n[start] show_inventory |", id,"\n")
    if not id in users.keys():
        await creat_id(ctx)
        await _player[id].msg.clear_reaction("\U0001F392")
    check_id(id)
    if len(users[id]['item']) == 0:
        await sendff(ctx,f"{users[id]['name']}의 가방","비어있음","green")
    else:
        result = f''
        for i in users[id]['item']:
            result = f"{result}{i} X {users[id]['item'][i]}\n"
        await sendff(ctx,f"{users[id]['name']}의 가방", result, "green")
    print(users[id]['name'],":",users[id]['item'])

    print("\n[end] show_inventory |", id,_player[id].name,_player[id].do_play,"\n")
    
async def show_me(ctx):
    id = ctx.message.author.id
    print("\n[start] show_me |", id,"\n")
    if id in users.keys():
        print("\n[start] show_me |", id,_player[id].name,_player[id].do_play,"\n")
        result = f"""name : {users[id]['name']}
money : {users[id]['money']}gold
atk : {users[id]['atk']}
hp : {users[id]['hp']}/{users[id]['hp_max']}
def : {users[id]['def']}
lv : {users[id]['lv']}
xp : {users[id]['xp']}/{users[id]['xp_max']}"""
        result = f"{result}\n가방을 확인하려면\"\U0001F392\"을 클릭하세요!"
        users[id]['item'] = {}
        _player[id].msg = await sendff(ctx, "내정보", result, "green")
        message_id_list[_player[id].msg.id] = id
        _player[id].do_play = "show_me"
        await _player[id].msg.add_reaction("\U0001F392")
        print("\n[end] show_me |", id,_player[id].name,_player[id].do_play,"\n")
    else:
        await creat_id(ctx)
        await show_me(ctx)
    print("\n[end] show_me |", id,_player[id].name,_player[id].do_play,"\n")

async def sendff(ctx, titlef, descriptionf, colorf):
    if (colorf == "red"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0xff0000))
    elif (colorf == "green"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x00ff00))
    elif (colorf == "blue"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x0000ff))

async def sendf(ctx, msg):
    return await ctx.send(msg)

def check_id(id):
    print(_player[id].id,_player[id].name,_player[id].do_play)



bot.run('MTA1NDIwNDI1Nzk2NTk3MzU2NQ.GvEZMs.D-4bI90UqETtLiWEgS5U-25-mqYDsk4TOM8p74') #test_dojin