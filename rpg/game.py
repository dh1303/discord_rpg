import discord
import asyncio
from discord.ext import commands
from random import randint

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents= intent)

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)    
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

# ===========================

class stat:
    def __init__(self, id) -> None:
        self.max_hp = 7
        self.hp = 7
        self.gold = 100
        self.attack = 1
        self.defense  = 1
        self.xp = 0
        self.max_xp = 4
        self.all_xp = 0
        self.lv = 1
        self.id = id
        pass

    def stat_lv(self):
        self.max_hp = 5 + (self.lv * 2)
        self.attack = 0.6 + (self * 0.4)
        self.defense = 0.8 + (self * 0.2)
        print("[stat_lv] max_hp :",self.max_hp,"| attack :",self.attack,"| defense :",self.defense,"| id :", self.id)

    def lv_up(self):
        while self.xp >= self.max_xp:
            self.lv += 1
            self.xp -= self.max_xp
            self.max_xp += (self.lv * 2)
            print("[lv_up] lv up 1","| id :", self.id)
        count = 1
        self.all_xp = 4
        while count <= self.lv:
            self.all_xp += (self.lv * 2)
        self.all_xp += self.xp
        self.stat_lv()
        print("[lv_up] all_xp :", self.all_xp,"| id :", self.id)

    def set(self, hp = None,max_hp = None, gold = None, attack = None, defense = None, xp = None, lv = None):
        if hp != None:
            self.hp = hp
            print("[set] hp :", hp,"| id :", self.id)
        if max_hp != None:
            self.max_hp = max_hp
            print("[set] max_hp :", max_hp,"| id :", self.id)
        if gold != None:
            self.gold = gold
            print("[set] gold :", gold,"| id :", self.id)
        if attack != None:
            self.attack = attack
            print("[set] attack :", attack,"| id :", self.id)
        if defense != None:
            self.defense = defense
            print("[set] defense :", defense,"| id :", self.id)
        if xp != None:
            self.xp = xp
            print("[set] xp :", xp,"| id :", self.id)
            self.lv_up()
        if lv != None:
            self.lv = lv
            print("[set] lv :", lv,"| id :", self.id)
            self.stat_lv()

    def get_stat(self):
        result = f"""gold : {self.gold}g
        hp : {self.hp}/{self.max_hp}
        attack : {self.attack}
        defense : {self.defense}
        xp : {self.xp}/{self.max_xp}({self.all_xp})
        lv : {self.lv}"""
        return result

class player:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.stat = stat(id)
        self.msg = {}
        self.inventory = {}
        pass

    def get_inventory(self):
        if len(self.inventory) == 0:
            return f"비어있음"
        else:
            result = f""
            for i in self.inventory.keys():
                result = f"{result}{i} X {self.inventory[i]}\n"
            return result

class stage:
    def __init__(self, monster, traesure, traesure_percentage) -> None:
        self.monster = monster
        self.traesure = traesure
        self.istraesure = traesure_percentage >= randint(1,100)
        pass

    def set_monster(self):
        print('ㅗ')

class item:
    def __init__(self, name, rank, price) -> None:
        self.name = name
        self.rank = rank
        self.price = price
        pass
    
class Shop:
    def __init__() -> None:
        pass
    
        
    
# ===========================

users = {}

text_list = {}

item_list = {"test1" : item("test1", "nomal", 15), 
             "test2" : item("test2", "rare", 50)}

# ================================

@bot.command()
async def test(ctx):
    print("[test] start")
    id = ctx.message.author.id
    name = ctx.message.author.name
    print("id :", id,"| name :", name)
    if not id in users.keys():
        users[id] = player(id, name)
        msg = await sendff(ctx, "계정 생성", f"name : {name}\n{users[id].stat.get_stat()}", "green")
        message_reaction(id, msg,'creat_id')
        await msg.add_reaction('🎒')
    else:
        await sendff(ctx, "계정 생성 오류", "계정이 이미 존재함", 'red')
    print(users)
    print("[test] end")

@bot.command()
async def me(ctx):
    print("[me] start")
    id = ctx.message.author.id
    name = ctx.message.author.name
    print("id :", id,"| name :", name)
    if id in users.keys():
        msg = await sendff(ctx, "내 정보", f"name : {name}\n{users[id].stat.get_stat()}", "green")
        message_reaction(id, msg,'me')
        await msg.add_reaction('🎒')
    else:
        await test(ctx)
    print("[me] end")
    
@bot.command()
async def shop(ctx):
    print("[shop] start")
    id = ctx.message.author.id
    name = ctx.message.author.name
    print("id :", id,"| name :", name)
    if id in users.keys():
        msg = await sendff(ctx, "상점", f"")
        
    
# ===============================

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        return None
    msg_id = reaction.message.id
    id = user.id
    ctx = reaction.message.channel
    print("msg_id :",msg_id,"| id :", id)
    print(text_list)
    if msg_id in text_list.keys():
        print(text_list[msg_id])
        if id == text_list[msg_id][0]:
            if text_list[msg_id][1] == "creat_id":
                if str(reaction.emoji) == "🎒":
                    await users[id].msg[msg_id].clear_reaction("🎒")
                    await sendff(ctx, f"{users[id].name}의 가방", users[id].get_inventory(),"green")
                    text_list.pop(msg_id)
                    users[id].msg.pop(msg_id)
                    print("text_list :", text_list)
                    print("msg :", users[id].msg)
            elif text_list[msg_id][1] == "me":
                if str(reaction.emoji) == "🎒":
                    await users[id].msg[msg_id].clear_reaction("🎒")
                    await sendff(ctx, f"{users[id].name}의 가방", users[id].get_inventory(),"green")
                    text_list.pop(msg_id)
                    users[id].msg.pop(msg_id)
                    print("text_list :", text_list)
                    print("msg :", users[id].msg)

 


# ==================================

def message_reaction(id, msg, do_play):
    text_list[msg.id] = [id, do_play]
    users[id].msg[msg.id] = msg

async def sendff(ctx, titlef, descriptionf, colorf):
    if (colorf == "red"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0xff0000))
    elif (colorf == "green"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x00ff00))
    elif (colorf == "blue"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x0000ff))
    elif (colorf == "black"):
        return await ctx.send(embed = discord.Embed(title= titlef, description = descriptionf, color = 0x000000))

async def sendfr(titlef, descriptionf, colorf):
    if (colorf == "red"):
        return discord.Embed(title= titlef, description = descriptionf, color = 0xff0000)
    elif (colorf == "green"):
        return discord.Embed(title= titlef, description = descriptionf, color = 0x00ff00)
    elif (colorf == "blue"):
        return discord.Embed(title= titlef, description = descriptionf, color = 0x0000ff)
    elif (colorf == "black"):
        return discord.Embed(title= titlef, description = descriptionf, color = 0x000000)

async def sendf(ctx, msg):
    return await ctx.send(msg)

bot.run('MTA1NDIwNDI1Nzk2NTk3MzU2NQ.GoXYii.s-D_6Ey3cXsORrEVCYZK8HFFeEg9_rqxopmLjU') #test_dojin