import os

import psutil
import platform
from datetime import datetime

from colorama import AnsiToWin32, Fore, init, Style
import discord
from discord.ext import commands, tasks
import json
import time, datetime
import time

init()

with open('config.json') as config_file: data = json.load(config_file)


def update_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

def update_timed():
    now = datetime.datetime.now()
    current_time = now.strftime("%D %Y %H:%M")
    return current_time


def read_json(filename):
    with open(f"{filename}.json", "r") as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4)




# Load config file
token = data['token']
role = data['support_role']
log = data['log_channel']
prefix = data['prefix']

bot = commands.Bot(command_prefix=f"{prefix}", intents=discord.Intents.all())
bot.remove_command("help")

print("""
   ____ _       _           _ _                 
  / ___| | ___ | |__   __ _| | |__   __ _ _ __  
 | |  _| |/ _ \| '_ \ / _` | | '_ \ / _` | '_ \ 
 | |_| | | (_) | |_) | (_| | | |_) | (_| | | | |
  \____|_|\___/|_.__/ \__,_|_|_.__/ \__,_|_| |_|
     Developer : Smash#1337    
                  
""")
data = read_json("bans")
if "ids" in data: # If there is no data in the bans file
        print(f"{Fore.GREEN}[{update_time()}] | {len(data['ids'])} users banned")
print(f"{Fore.GREEN}[{update_time()}] | Starting Globalban System...")
print(f"{Fore.GREEN}[{update_time()}] | Started!")
print("================================================================")
print()


@bot.event
async def on_ready(cpufreq=None):
    channel = bot.get_channel(int(log))           
    embed = discord.Embed(title=f"Globalban System", description=f"Bot started on NODE-1 ", color=2303786)
    embed.set_footer(text="Globalban System - 2022")
    await channel.send(embed=embed)
    print(f"{Fore.GREEN}[{update_time()}] | Started on {psutil.cpu_freq().max:.1f}Mhz")
    print(f"{Fore.GREEN}[{update_time()}] | Connected to Discord as {bot.user.name}")
    print(f"{Fore.GREEN}[{update_time()}] | Connected to Discord API!")
    print()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                name=f"Over {len(set(bot.users))} User's Protected | Over {len(bot.guilds)} Server's Protected"))

@bot.command() # your client/bot variable. IDK which you have so I put bot.
async def ff(ctx):
    guilds = {len(guild.members):guild for guild in bot.guilds}
    max_members, max_guild = max(guilds.items())
    await ctx.send(f"{max_guild.name} is the biggest server I am in! They have {max_members} members!")

@bot.event
async def on_command_error(ctx, error): # Error handling
    if isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title=f"Global System", description=f"Command not found, usage ``{prefix}help``", color=2303786)
        em.set_footer(text="Globalban System - 2022")
        await ctx.send(embed=em) # Send the error to the same channel as the command


@bot.event
async def on_member_join(user: discord.User):
    if time.time() - user.created_at.timestamp() < 432000: # check if user is younger than 5 days
            embed = discord.Embed(title=f"Globalban System",
                                description=f"Your account is too young Your account must be older than 5 days",
                                color=2303786)
            embed.add_field(name='Account created:', value=user.created_at)
            embed.add_field(name=f"Reason:", value=f"```Your account is too young!```", inline=False)
            embed.set_footer(text="If you have any questions about your ban, get in touch With our support team")
            await user.send(embed=embed)
            await user.kick() # kick user if he is younger than 5 days
    else:
            print(f"{Fore.GREEN}[{update_time()}] {user} joined the server") # print user joined the server
        

    data = read_json("bans")  # Load bans file
    data["ids"]
    if user.id in data["ids"]: # check if user is banned
        channel = bot.get_channel(int(log))       # get log channel
        embed = discord.Embed(title=f"Globalban System",
                              description=f"``{user.name}`` is banned and try to join ``{user.guild.name}``",
                              color=2303786)
        embed.set_footer(text="Globalban System - 2022")
        await channel.send(embed=embed)

        embed = discord.Embed(title=f"Globalban System",
                              description=f"You have been permanently banned from `{len(bot.guilds)}` servers", 
                              color=2303786)
        embed.add_field(name=f"Reason:", value=f"```Automatic Kick```", inline=False)
        embed.set_footer(text="If you have any questions about your ban, get in touch With our support team") # Send the error to the same channel as the command
        await user.send(embed=embed) # send ban message to user
        await user.kick() # kick user if he is banned

        print(f"{Fore.RED}[{update_time()}] [-] {user.name}({user.id}) Is Banned And Tryed To Join {user.guild.name}({user.guild.id})") # print user banned and tryed to join the server
    else: # if user is not banned
        channel = bot.get_channel(int(log))     
        embed = discord.Embed(title=f"Globalban System",
                              description=f" {user.name}({user.id}) Joined {user.guild.name}({user.guild.id})",
                              color=2303786)
        embed.set_footer(text="Globalban System - 2022")
        await channel.send(embed=embed) # Send the error to the same channel as the command

        print(f"{Fore.GREEN}[{update_time()}] [+] {user.name}({user.id}) Joined {user.guild.name}({user.guild.id})") # print user joined the server
 
 
 
 
 

@bot.command()
async def gban(ctx, user: discord.User, reason="No reason given"):
    smash = discord.utils.get(ctx.guild.roles, id=int(role))     # Get the role
    if smash in ctx.author.roles: # check if user has the support role
            data = read_json("bans")  # Load data
            data["ids"] # Load ids
            if user.id in data["ids"]:
                embed = discord.Embed(title=f"Globalban System",
                                    description=f"I can't ban user ``{user.name}`` because he is already banned", color=2303786)
                embed.set_footer(text="Globalban System - 2022")
                await ctx.send(embed=embed)
                pass
            else: # if user is not banned
                embed = discord.Embed(title=f"Globalban System",
                                    description=f"The user ``{user.name}`` is now banned from ``{len(bot.guilds)}`` servers for the reason: ``{reason}``",
                                    color=2303786)
                embed.set_footer(text="Globalban System - 2022") 
                await ctx.send(embed=embed) # Send the error to the same channel as the command
                data["ids"].append(user.id) # Add user to banned list
                write_json(data, "bans") # Write data

                channel = bot.get_channel(int(log))      # Send message to the channel
                embed = discord.Embed(title=f"Globalban System",
                                    description=f"The member ``{user.name}`` has been banned from ``{len(bot.guilds)}`` servers",
                                    color=2303786)
                embed.set_footer(text="Globalban System - 2022") # Send the error to the same channel as the command
                await channel.send(embed=embed)
                print(f"{Fore.GREEN}[{update_time()}] [+] {user.name} | {user.id} is now on {len(bot.guilds)} servers! banned | Reason: {reason}") # print user banned

            try: # Try to kick the user
                embed = discord.Embed(title=f"Globalban System",
                                    description=f"You have been permanently banned from `{len(bot.guilds)}` servers", 
                                    color=2303786)
                embed.add_field(name=f"Reason:", value=f"```{reason}```", inline=False) # Send the error to the same channel as the command
                embed.add_field(name=f"Banned By:", value=f"```{ctx.author} - {ctx.author.id}```", inline=False) # print banned user
                await user.send(embed=embed) # Send the error to the same channel as the command
                await user.send(f"if you want to make a Unban request, get in touch With our support team") # send user a message to make a unban request
                for guild in bot.guilds:
                    try:
                        await guild.ban(user, reason=reason) # ban user from all servers
                    except: # if user is owner of the server
                        print(f"I don't have permission to bans= in {guild}")
                        pass
            except: # if the user has no DM's
                for guild in bot.guilds:
                    try:
                        await guild.ban(user, reason=reason) # ban user from all servers
                    except: # if user is owner of the server
                        print(f"I don't have permission to bans= in {guild}")
                        pass
                embed = discord.Embed(title=f"Globalban System", description=f"I can't write privately to a member, maybe he has his direct messages off or isn't on the servers where I'm on",
                                    color=2303786)
                embed.set_footer(text="Globalban System - 2022")
                
                await ctx.send(embed=embed) # Send the error to the same channel as the command
                
@bot.command()
async def gunban(ctx, user: discord.User): # unban command
    smash = discord.utils.get(ctx.guild.roles, id=int(role)) # get role
    if smash in ctx.author.roles: # if user has role
            data = read_json("bans") # load data
            data["ids"].remove(user.id) # remove user id from data
            write_json(data, "bans") # write data 
            embed = discord.Embed(title=f"Globalban System", # create embed
                                description=f"``{user.name}`` is now on ``{len(bot.guilds)}`` servers unbanned.", color=2303786)
            embed.set_footer(text="Globalban System - 2022")
            await ctx.send(embed=embed) # send embed

            channel = bot.get_channel(int(log))      # get log channel
            embed = discord.Embed(title=f"Globalban System", description=f"``{user.name}`` is now on ``{len(bot.guilds)}`` servers unbanned.",
                                color=2303786)
            embed.set_footer(text="Globalban System - 2022")
            await channel.send(embed=embed)
            for guild in bot.guilds: # for every guild
                try:
                    await guild.unban(user) # unban user
                except: # if user is not on the server
                    print(f"I don't have permission to unban in {guild}")
                    pass


@bot.command()
async def stats(ctx): # Stats Command
    data = read_json("bans")
    if "ids" in data: # If there is no data in the bans file
        embed = discord.Embed(title=f"Globalban Stats", color=2303786)
        embed.add_field(name=f"Total users banned: ", value=f"{len(data['ids'])}", inline=True)
        embed.add_field(name=f"Total servers: ", value=f"{len(bot.guilds)} servers", inline=False)
        embed.add_field(name='CPU Usage: ', value=f'{psutil.cpu_percent()}%', inline=False)
        embed.add_field(name='Memory Usage: ', value=f'{psutil.virtual_memory().percent}%', inline=False)
        embed.add_field(name='Available Memory: ',
                        value=f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}%',
                        inline=False)
        await ctx.send(embed=embed) # Send the embed

@bot.command()
async def check(ctx, user: discord.User):
    w = read_json("w")  # Load data
    w["ids"] # Load ids
    data = read_json("bans")  # Load data
    data["ids"] # Load ids
    if user.id in data["ids"]: # If user is banned
        embed = discord.Embed(title=f"Userinfo From {user.name}", color=2303786)
        embed.add_field(name=f"Is the User Globalbanned: ", value=f"Yes", inline=True)
        await ctx.send(embed=embed)
    if user.id not in data["ids"]:
        embed = discord.Embed(title=f"Userinfo From {user.name}", color=2303786)
        embed.add_field(name=f"Is the User Globalbanned: ", value=f"No", inline=True)
        await ctx.send(embed=embed)


@bot.command()
async def servers(self, ctx):
    activeservers = bot.guilds
    for guild in activeservers:
        await ctx.send(guild.name)

@bot.command()
async def ping(ctx): # Ping Command
    if round(bot.latency * 1000) <= 50: # If the latency is less than 50ms
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: The ping is **{round(bot.latency * 1000)}** milliseconds!",
                              color=0x44ff44)
    elif round(bot.latency * 1000) <= 100: # If the latency is less than 100ms
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: The ping is **{round(bot.latency * 1000)}** milliseconds!",
                              color=0xffd000)  
    elif round(bot.latency * 1000) <= 200: # If the latency is less than 200ms
        embed = discord.Embed(title="PING",
                              description=f":ping_pong: The ping is **{round(bot.latency * 1000)}** milliseconds!",
                              color=0xff6600)
    else:
        embed = discord.Embed(title="PING", # If the latency is more than 200ms
                              description=f":ping_pong: The ping is **{round(bot.latency * 1000)}** milliseconds!",
                              color=0x990000)
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx): # Help Command
    HelpEmbed = discord.Embed(
        title="Help & Support :question:",
        description=
        "Here is you can find instructions of how to use the bot! \n\n If you are not satisfied, visit our discord [Invite](https://discord.gg/wvfgSgg9bc)",
        color=2303786)
    HelpEmbed.add_field(
        name=".stats",
        value=
        "```This command will show you the stats of the bot!```",
        inline=False)
    HelpEmbed.add_field(
        name=".ping",
        value=
        "```This command will show you the ping of the bot!```",
        inline=False)
    HelpEmbed.add_field(
        name=".gban",
        value=
        "```This command will ban a user from all servers ~ Only for admins```",
        inline=False)
    HelpEmbed.add_field(
        name=".gunban",
        value=
        "```This command will unban a user from all servers ~ Only for admins```",
        inline=False)

    await ctx.send(embed=HelpEmbed)


bot.run(token) # Run the bot