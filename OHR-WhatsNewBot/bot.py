import discord
from urllib.request import urlopen
import textwrap
import time
from discord.ext import commands, tasks
import os
import json

NIGHTLY_WHATSNEW_URL = "https://raw.githubusercontent.com/ohrrpgce/ohrrpgce/wip/whatsnew.txt"
RELEASE_WHATSNEW_URL = "https://hamsterrepublic.com/ohrrpgce/whatsnew.txt"
APP_TOKEN = ""
SAVE_FOLDER = os.path.dirname(os.path.realpath(__file__))
MAX_CONTENT_LENGTH = 2000-6 # -6 to supply block formatting.
MSG_DELAY = 3
END_OF_UPDATE_TEXT = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
client = commands.Bot(command_prefix='!')

with open (os.path.join(SAVE_FOLDER,"config.json"),'r') as fi:
    CONFIG = json.load(fi)

APP_TOKEN = CONFIG["APP_TOKEN"]
time_ticker = 0


def save_whatsnew(url=None,text_content=None):
    if url == NIGHTLY_WHATSNEW_URL:
        fn = "nightly.txt"
    if url == RELEASE_WHATSNEW_URL:
        fn = "release.txt"
    
    with open (os.path.join(SAVE_FOLDER, fn),'w') as fo:
        for each_line in text_content: # this is a list
            fo.write(each_line)
        print ("Updated "+fn)


def get_whatsnew(url=None,save_update=False):
    if url == NIGHTLY_WHATSNEW_URL or url == NIGHTLY_WHATSNEW_URL:
        content = urlopen(url).read()
        content = (content.decode('utf-8'))
        content = content.split("*** New Features")
        content = content[0] + content[1] # Should just be the most recent release/WIP release.
        split_string = textwrap.wrap(content, MAX_CONTENT_LENGTH,replace_whitespace=False,break_long_words=False)
        for each_text in END_OF_UPDATE_TEXT:
            if each_text in split_string[-1].lower():
                del split_string[-1]
        
        if save_update == True:
            save_whatsnew(url=url,text_content=split_string)
        
        return split_string
    else:
        return None

def get_just_changes(url=None):
    if url == NIGHTLY_WHATSNEW_URL:
        fn = "nightly.txt"
    elif url == RELEASE_WHATSNEW_URL:
        fn = "release.txt"
    else:
        return None
    
    with open (os.path.join(SAVE_FOLDER, fn),'r') as fi:
        old_whatsnew = fi.readlines()

    get_whatsnew(url=url,save_update=True)

    with open (os.path.join(SAVE_FOLDER, fn),'r') as fi:
        new_whatsnew = fi.readlines()

    new_updates = list()
    for each in new_whatsnew:
        if each in old_whatsnew:
            pass
        else:
            new_updates.append(each)

    return new_updates


@commands.cooldown(rate=1, per=30, type=commands.BucketType.guild)
@client.command(name='whatsnew',help='Retrieves and displays the most recent nightly/release version of whatsnew.txt from HamsterRepublic.')
async def whatsnew(ctx,release_or_nightly:str):
    if release_or_nightly.lower() == "release":
        url_to_use = RELEASE_WHATSNEW_URL

    if release_or_nightly.lower() == "nightly":
        url_to_use = NIGHTLY_WHATSNEW_URL

    if release_or_nightly.lower() == "release" or release_or_nightly.lower() == "nightly":
    # SENDS BACK A MESSAGE TO THE CHANNEL.
        msg = get_whatsnew(url=url_to_use,save_update=True)
        await ctx.send(f"{release_or_nightly} Whatsnew: {url_to_use}\n----------")
        for each in msg: 
            await ctx.send("```"+each+"```")
            time.sleep(MSG_DELAY)

@commands.cooldown(rate=1, per=30, type=commands.BucketType.guild)
@client.command(name='nightly_updates',help="Just displays and updates what is new in the update, not the entire nightly.")
async def nightly_updates(ctx):
    msg = get_just_changes(url=NIGHTLY_WHATSNEW_URL)
    if len(msg) < 1:
        await ctx.send(f"No changes in nightly, sorry!")
    else:
        await ctx.send(f"Nightly changes\n----------")    
        for each in msg: 
            await ctx.send(each)
            time.sleep(MSG_DELAY)


@client.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in client.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("OHRRPGCE What's New Bot is in " + str(guild_count) + " guilds.")

@client.event
async def on_message(message):
    if(message.author == client.user):
        return
    try:
        await client.process_commands(message)
    except:
        if "!whatsnew" in message:
            print ("Supplied !whatsnew without argument.")


@tasks.loop(hours=24)
async def called_once_a_day():
    global time_ticker
    time_ticker=time_ticker+1
    if time_ticker < 8: # This is to prevent discords awful task system from exploding when starting up.
        return None     # Otherwise it gets about halfway through this routine 8 times when you start up.
    print ("Triggered.")
    text_channel_list = []
    for guild in client.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)

    for message_channel in text_channel_list:      
        print(f"Got channel {message_channel}")
        msg = []
        msg = get_just_changes(url=NIGHTLY_WHATSNEW_URL)
        if msg == []: 
            print ("No new updates.")
        else:
            print ("Posting updates in available chats.")
            for each in msg:
                try:
                    await message_channel.send(msg)
                    time.sleep(MSG_DELAY)
                except:
                    print ("Couldn't post message in "+message_channel)
                    pass
    
@called_once_a_day.before_loop
async def before():
    print("Preparing scheduled task...")
    await client.wait_until_ready()
    



called_once_a_day.start()
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
client.run(APP_TOKEN)

