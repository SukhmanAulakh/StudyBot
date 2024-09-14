import discord
from discord.ext import commands
import requests
import os
import re

TOKENS = open('Token.txt','r')
DiscTOKEN = TOKENS.readline()
TOKENS.close()

##Initalize DATA FILE
needNewLine = False
DATA = open('Data.txt','r')
allowedActs=list()
lastline =""
for line in DATA:
    lastline = line
    if line.endswith("\n"):
        line=line[:-1]
    if len(line)>0:
        allowedActs.append(line)
DATA.close()
print(allowedActs)
##CHECK IF LAST LINE HAS \n element so new elements will be appended correctly
if not lastline.endswith("\n") and lastline != "":
    DATA = open('Data.txt','a')
    DATA.write("\n")
    DATA.close()
    print("Added \\n")

prevAct="default"

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='$',intents=intents)

shutdown=False

#Process Discord Event
@client.event
async def on_ready():
    print("We Have logged in as: {0.user}".format(client))

@client.event
async def on_presence_update(before, after):
    prevAct = before.activity.name

    if after.activity == None:
        return
    
    else:
        beforeActs = before.activities
        afterActs = after.activities
        difActs = set(afterActs).symmetric_difference(set(beforeActs))

        for act in difActs:
            if act.type == discord.ActivityType.playing and act.name not in allowedActs and act.name!=prevAct:
                prevAct=act.name
                await after.send(after.name + " are you studying right now???? Because it seems you are playing "+ act.name)
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    text = message.content
    
    if text.startswith('$hello'):
        await message.channel.send('Hello!!!')

    elif text.startswith('$help'):
        await message.channel.send('Bot That Helps You Notice How Often You Become Distracted.\n'
                                   +'$AddException <"Name of Application">\n'
                                   +'$RemoveException <"Name Of Application">\n'
                                   +'$ListExceptions\n'
                                   +'$mute')

    elif text.startswith('$AddException'):
        exceptionStr = text.replace("$AddException","").replace(" ","",1)
        if(len(exceptionStr)>0):
            repeatingElement = False
            for act in allowedActs:
                if exceptionStr == act:
                    repeatingElement = True
            if not repeatingElement:
                DATA = open('Data.txt','a')
                DATA.write(exceptionStr+"\n")
                DATA.close()
                allowedActs.append(exceptionStr)
                await message.channel.send(exceptionStr+" :Added")
        else:
            await message.channel.send("Must be in Form '$AddException NAMEOFEXCEPTION'")

    elif text.startswith('$RemoveException'):
        exceptionStr = text.replace("$RemoveException","").replace(" ","",1)
        if(len(exceptionStr)>0):
            repeatingElement = False
            for act in allowedActs:
                if exceptionStr == act:
                    repeatingElement = True
                    allowedActs.remove(act)
            if repeatingElement:
                DATA = open('Data.txt','w')
                for act in allowedActs:
                    DATA.write(act+"\n")
                DATA.close()
                await message.channel.send(exceptionStr+" :Removed")
            else:
                await message.channel.send("No Exception Found Called: "+exceptionStr)

        else:
            await message.channel.send("Must be in Form '$RemoveException NAMEOFEXCEPTION'")

    
    elif text.startswith('$ListExceptions'):
        for act in allowedActs:
            await message.channel.send(act)
        if len(allowedActs)==0:
            await message.channel.send("No Exceptions Found: Please Add Exeptions Via '$AddException NAMEOFEXCEPTION'")
    
    elif text.startswith('$ClearExceptions'):
        allowedActs.clear()
        DATA = open('Data.txt','w')
        DATA.write("")
        DATA.close()
        await message.channel.send("Cleared All Exceptions")
    
    elif text.startswith('$mute'):
        await message.channel.send('Hello!!!')
    
    elif text.startswith('$shutdown'):
        shutdown=True
        await message.channel.send('byeee!!!')
        print("Bot Closed")
        await client.close()

if(shutdown==False):
    client.run(DiscTOKEN)