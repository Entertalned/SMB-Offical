import discord
import os
import random
import datetime
import asyncio
import json
import time 
import re
from discord.utils import get
from operator import itemgetter

from discord.ext import commands
intents = discord.Intents.all()
intents.members = True
bot = discord.Bot(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
bot = discord.Bot(debug_guilds=[]) 

@bot.event
async def on_ready():
    servers = {len(bot.guilds)}
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
        print(guild.name, guild.member_count)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} Servers| {members} Members| /help"))
#Main Directory
@bot.slash_command(description="Shows You The Commands In A Easy-To-Read List.")
@commands.guild_only()
async def help(ctx):
    embed = discord.Embed(
        title="My Commands Are",
        description="Prefix Is /",
        colour=0xFF0000
        )
    embed.set_thumbnail(url="https://i.gyazo.com/ae6a40f3407f80097e78115d8538f7ab.jpg")
    embed.add_field(name="━━━━━━━━━━**Commands**━━━━━━━━━━━", value="say, serverstats, whois, host, coinflip, 8ball, diceroll, embedcreate, suggest, simpdetector, botinfo, pms, report, leaderboard, dleaderboard, runtime", inline=False)
    embed.add_field(name="━━━━━━━━**Moderation Commands**━━━━━━━━", value="purge, mute/unmute, lockdown/unlock, setrc, setsc ban/unban, kick", inline=False)
    embed.add_field(name="━━━━━━━━**Calculation Commands**━━━━━━━━", value="add, subtract, divide, multiply", inline=False)
    embed.add_field(name=f"Need Help?", value=f"Join the [Discord](https://discord.gg/3ay4JH6d9Q) server, Or do {dsuggest.mention}")
    embed.add_field(name=f"Want All The Commands In Detail??", value=f"Checkout the github which includes [Detailed Commands](https://github.com/SlimsBotAndSuch/Commands/blob/main/In%20Detail) And Our [Changelog](https://github.com/SlimsBotAndSuch/changelog/blob/main/Official%20Changelog%20For%20SMB)")
    embed.set_footer(text=f"Requested By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
#Runtime
@bot.command(pass_context=True)
@commands.guild_only()
async def runtime(ctx):
    now = datetime.datetime.now()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(
    title="Runtime",
    description="Running for {}d {}h {}m {}s".format(elapsed.days, hours, minutes, seconds),
    color=0xFF0000
    )
    embed.set_footer(text="If You Were Wondering")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
starttime = datetime.datetime.now()                
#Small Commands
@bot.command(description="Make The Bot Say What You Type.")
async def say(ctx, *, message):
    try:
        await ctx.respond(message)
    except:
        await ctx.respond("Please Give Some Message!")
        
@bot.command(description="Keeps you hidden while sending a server a private message.")
@commands.guild_only()
async def pms(ctx, *, message):
    await ctx.send(message)
    embed = discord.Embed(
    title="Message sent!",
    description="",
    colour=0xFF0000
    )
    await ctx.respond(embed=embed, ephemeral=True)
        
@bot.command(description="Adds 2 Numbers.")
async def add(ctx, add: int, to: int):
    await ctx.respond(add + to)
    
@bot.command(description="Subtracts 2 Numbers.")
async def subtract(ctx, subtract: int, by: int):
    await ctx.respond(subtract - by)
             
@bot.command(description="Divides 2 Numbers.")
async def divide(ctx, divide: int, by: int):
    await ctx.respond(divide / by)
    
@bot.command(description="Multiply 2 Numbers.")
async def multiply(ctx, multiply: int, by: int):
    await ctx.respond(multiply * by)
    
@bot.command(description="Purge A Max Amount Of 1000 Messages.")
@commands.has_guild_permissions(manage_messages=True)
@commands.guild_only()
async def purge(ctx, limit: int):
    if limit > 1000:
        await ctx.send("You can only purge up to 1000 messages")
        return
    elif limit < 1:
        await ctx.send("You must purge at least 1 message")
        return
    await ctx.channel.purge(limit=limit)
    embed = discord.Embed(
    title=f"Channel Purged!",
    description=f"{ctx.author.mention} Purged {limit} Messages.",
    color=0xFF0000
    )
    await ctx.respond(embed=embed)
#Large Embeds(End of small commands.)
@bot.command(description="Show's Detail's Of Your Current Server.")
@commands.guild_only()
async def serverstats(ctx):
    date_format = "%a, %b %d, %Y @ %I:%M %p" 
    embed = discord.Embed(
        title=f"{ctx.guild.name}",
        description=f"{ctx.guild.id}",
        colour=0xFF0000
        )
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name="Owner:", value=ctx.guild.owner)
    embed.add_field(name="Members:", value=ctx.guild.member_count)
    embed.add_field(name="Created @", value=f"{ctx.guild.created_at.strftime(date_format)}")
    embed.add_field(name="Channels:", value=f" **Text Channels:** {len(ctx.guild.text_channels)}, **Voice Channels:** {len(ctx.guild.voice_channels)}, **Catagories:** {len(ctx.guild.categories)}")
    embed.add_field(name="Roles:", value=f"{len(ctx.guild.roles)}")
    embed.add_field(name="Total Boosters:", value=f"{str(ctx.guild.premium_subscription_count)}")
    embed.set_footer(text=f"If Owner Returns As None, It Just Means The Owner Was Offline When The Bot Joined.")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
    
@bot.command(description="Shows A Mentioned Members Details.")
@commands.has_permissions(send_messages=True)
@commands.guild_only()
async def whois(ctx, member: discord.Member):
    roles = [role for role in member.roles[1:]]
    joined_at = member.joined_at.strftime("%a, %b %d, %Y @ %I:%M %p")
    date_format = "%a, %b %d, %Y @ %I:%M %p" 
    embed = discord.Embed(
      title=f"{member}",   
      description=f"Here Is {member}'s Info!",
      colour=0xff0000
      )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name=f"Display Name", value=f"{member.display_name}")
    embed.add_field(name=f"Joined @", value=f"{joined_at}")
    embed.add_field(name=f"Created @", value=f"{member.created_at.strftime(date_format)}")
    embed.add_field(name=f"Roles", value=f"".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Permission Check", value=f"**Admin** {member.guild_permissions.administrator}, **Ban Members** {member.guild_permissions.ban_members}, **Kick Members** {member.guild_permissions.kick_members}, **Read Message History**{member.guild_permissions.read_message_history}", inline=True)
    embed.set_footer(text=f"ID: {member.id} Requested By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
#Start Bots Offical Host
@bot.command(description="Shows The Offical Host For SMB.")
async def host(ctx):
    embed = discord.Embed(
        title="Offical Host",
        description="Ever Heard Of Lightbulb Hosting?",
        colour=0xFF0000
        )
    embed.set_thumbnail(url="https://i.gyazo.com/e4aa08843e35bc75649c86d7de610709.png")
    embed.add_field(name="Lightbulb", value="[Lightbulb](https://discord.gg/aE4csQzQey) Is a bot hosting website, allowing users to make a bot for free for no price at all. However they are closed to new members as of this moment.")
    embed.set_footer(text=f"Requested By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
#Start Moderation Commands
@bot.command(description="It bans a member with the mighty ban hammer, and sends a dm of the reason.")
@commands.has_permissions(ban_members=True) 
@commands.guild_only()
async def ban(ctx, member: discord.Member ,*, reason=None):
    if member == ctx.author:
        await ctx.send("You can't ban yourself")
        return
    if member.id == (725864070804144148):
        await ctx.send("Really dude... That's just disrespectful to ban the owner of the bot with his own bot.")
        return
    embedm = discord.Embed(
    title="You were banned!",
    description=f"{ctx.author.mention} banned you from {ctx.author.guild}",
    color=0xFF0000
    )
    embedm.timestamp = datetime.datetime.now()
    embedm.add_field(name="**Server Owner Contact:**", value=ctx.guild.owner.mention)
    embedm.add_field(name="**Reason:**", value=reason)
    embedm.add_field(name="**Channel:**", value=ctx.channel.mention)
    embedm.set_footer(text="If you feel you've been banned for no reason, you can contact the moderator or the owner.")
    embedm.timestamp = datetime.datetime.now()
    await member.send(embed=embedm)
    await ctx.guild.ban(member, reason=reason)
    embed = discord.Embed(
     title="Member Banned!",
     description=f"{member.mention} was banned by {ctx.author.mention}",
     color=0xFF0000
    )
    embed.timestamp = datetime.datetime.now()
    embed.add_field(name="**Reason:**", value=reason)
    await ctx.respond(embed=embed) 
@ban.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the mute command")
        await ctx.respond("I'm sorry, but you need ban member's permission to use this command :c")
    else:
        raise error 

@bot.command(description="Unbans a member")
@commands.has_permissions(ban_members=True)
@commands.guild_only()
async def unban(ctx, userid: discord.User, reason=None):
    await ctx.guild.unban(userid)
    embed = discord.Embed(
     title="Member Unbanned!",
     description=f"{ctx.author.mention} unbanned {userid}",
     color=0xFF0000
    )
    embed.add_field(name="**Reason**:", value=reason)
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)  
    embedm = discord.Embed(
     title="Member Unbanned!",
     description=f"{ctx.author.mention} Unbanned You From {ctx.guild.name}",
     color=0xFF0000
    )
    embedm.add_field(name="**Reason**:", value=reason)
    embedm.set_footer(text="Just Don't Do What You Did Again.")
    embedm.timestamp = datetime.datetime.now()
    await userid.send(embed=embedm)
@unban.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the mute command")
        await ctx.respond("I'm sorry, but you need ban member's permission to use this command :c")
    else:
        raise error     
          
@bot.command(description="Warns A Mentioned Member")
async def warn(ctx, member = discord.Member, reason = None):
    with open('warns.json','r') as f:
            users = json.load(f)
            if ctx.guild.name not in users:
                users[ctx.guild.name] = {}
            try:
                users[ctx.guild.name][member] += 1
            except KeyError:
                users[ctx.guild.name][member] = 1
            with open('warns.json','w') as f:
                json.dump(users,f,indent=4)   
                embed = discord.Embed(
                title="User Warned!",
                description=f"{member} Was Warned By {ctx.author.mention}",
                color=0xFF0000
                )
                embed.add_field(name="**Reason**", value=reason)
                embed.set_footer(text=f"Do /swarns To See Your Server's Warns")
                embed.timestamp = datetime.datetime.now()
                await ctx.respond(embed=embed)

@bot.command(description="Warn Count")
@commands.cooldown(1, 20, commands.BucketType.user) 
async def swarns(ctx):
	listValues = []
	sortedList = []

	embed = discord.Embed(
			 title="Server Warns",
			 description=f"{ctx.guild.name}**",
			 color=0x9b0000
			)
	
	with open('warns.json') as file:
		data = json.load(file)
		listValues = new_list = list(map(list, data[f"{ctx.guild.name}"].items()))
		
	sortedList = sorted(listValues, key=itemgetter(1), reverse=True)
	strToPrint = ""
	for item in sortedList : 
		strToPrint = strToPrint +"\n"+ item[0] +" : "+str(item[1])  
	embed.add_field(name="━━━━━━━━━━━𝐖𝐀𝐑𝐍𝐒━━━━━━━━━━━", value=f"**{strToPrint}**" )
	embed.set_footer(text="Hopefully Not TO Many.....Right?")
	await ctx.respond(embed=embed)      
            
		
		
		
		

		
		
		
		
@bot.command(description="Kick a member with da boot!")
@commands.has_permissions(kick_members=True) 
@commands.guild_only()
async def kick(ctx, member: discord.Member ,*, reason=None):
    if member == ctx.author:
        await ctx.send("You can't kick yourself")
        return
    if member.id == (725864070804144148):
        await ctx.send("Really dude... That's just disrespectful to kick the owner of the bot with his own bot.")
        return
    embedm = discord.Embed(
    title="You were kicked!",
    description=f"{ctx.author.mention} kicked you from {ctx.author.guild}",
    color=0xFF0000
    )
    embedm.timestamp = datetime.datetime.now()
    embedm.add_field(name="**Reason:**", value=reason)
    await member.send(embed=embedm)
    await ctx.guild.kick(member, reason=reason)
    embed = discord.Embed(
         title="Member Kicked!",
         description="{ctx.authorn.mention} Kicked {ctx.member.mention}",
         color=0xFF000
         )
    embed.add_field(name="**Reason:**", value=reason)
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
      
@bot.command(description="Mutes A Mentioned Member And Sends It To Your Log Channel!")
@commands.has_permissions(kick_members=True,)
@commands.guild_only()
async def mute(ctx, member: discord.Member ,*, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    embed = discord.Embed(
     title="User Was Muted!",
     description=(f"{ctx.author.mention} Muted {member.mention}"),
     colour=(0xff0000)
    )
    embed.add_field(name="**Reason:**", value=(reason))
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
    embedm = discord.Embed(
    title="You Were Muted!",
    description=f"{ctx.author.mention} Muted you in {ctx.author.guild}",
    color=0xFF0000
    )
    embedm.timestamp = datetime.datetime.now()
    embedm.add_field(name="**Reason:**", value=reason)
    embedm.add_field(name="**Channel:**", value=ctx.channel.mention)
    await member.send(embed=embedm)
@mute.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the mute command")
        await ctx.respond("I'm sorry, but you need kick member's permission to use this command :c")
    else:
        raise error 

@bot.command(description="Unmutes A Mentioned Member.")
@commands.has_permissions(kick_members=True)
@commands.guild_only()
async def unmute(ctx, member: discord.Member ,*, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    embed = discord.Embed(
      title=f"User Unmuted!",
      description=(f"{ctx.author.mention} Unmuted {member.mention}"),
      colour=(0xff0000)
      )
    embed.add_field(name="**Reason:**", value=reason)
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
    embedu = discord.Embed(
    title="You Were Unmuted!",
    description=f"{ctx.author.mention} Unmuted you in {ctx.author.guild}",
    color=0xFF0000
    )
    embedu.timestamp = datetime.datetime.now()
    embedu.add_field(name="**Reason:**", value=reason)
    embedu.add_field(name="**Channel:**", value=ctx.channel.mention)
    embedu.set_footer(text="Try not to do whatever you did.")
    await member.send(embed=embedu)
@unmute.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the unmute command")
        await ctx.respond("I'm sorry, but you don't have kick members permissions :c")
    else:
        raise error   

@bot.command(description="Locks Down A Specified Channel.")
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def lockdown(ctx, reason):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    embed = discord.Embed(
      title=f"Channel Locked!",
      description=f"{ctx.channel.mention} Was Locked By {ctx.author.mention}",
      colour=(0x0000ff)
      )
    embed.add_field(name=f"Reason", value=(reason))
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
@lockdown.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the lockdown command")
        await ctx.respond("I'm sorry, but you don't have manage channel permissions :c")
    else:
        raise error 
    
@bot.command(description="Unlocks A Specified Channel.")
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def unlock(ctx, reason):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(
      title="Channel Unlocked!",
      description=f"{ctx.channel.mention} Was Unlocked By {ctx.author.mention}",
      colour=(0x0000ff)
      )
    embed.add_field(name="Reason", value=(reason))
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
@unlock.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the unlock command")
        await ctx.respond("I'm sorry, but you don't have manage channel permissions :c")
    else:
        raise error 

@bot.command(description="Sets a report channel for your member's to report other misbehaviors.")
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def setrc(ctx, channels: discord.TextChannel):
    with open('report_channels.json','r') as f:
        channelss = json.load(f)

    channelss[str(ctx.guild.id)] = int(channels.id)

    with open('report_channels.json','w') as f:
        json.dump(channelss,f,indent=4)

    await ctx.send(f"set the report channel to {channels}")  
@setrc.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.MissingPermissions):
        print(f"A error occured from {ctx.author} trying to use the setrc command")
        await ctx.respond("I'm sorry, but you don't have manage channel permissions :c")
    else:
        raise errors 

@bot.slash_command(description="Report a user for being a bad boy, only works if you have set a report channel.")
@commands.cooldown(1, 1800, commands.BucketType.user) 
@commands.guild_only()
async def report(ctx, member:discord.Member, *, reason):
    with open('report_channels.json', 'r') as f:
        channelss = json.load(f)


    channel_log = ctx.guild.get_channel(channelss[str(ctx.guild.id)])
    embed = discord.Embed(
        title="Report",
        description=f"**{ctx.author}** Has Reported **{member}**",
        color=0xFF0000
    )
    embed.add_field(name="**Reason:**", value=reason)
    embed.timestamp = datetime.datetime.now()
    await channel_log.send(embed=embed)
    await ctx.respond("**Report Sent Successfully!**", ephemeral=True)
@report.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("You can only send one report every 30 minutes!")
    else:
        raise error         
#TODO ASAP    
@bot.command(description="Sets a suggestion channel for your member's to report other misbehaviors.")
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def setsc(ctx, channels: discord.TextChannel):
    with open('suggestionchannels.json','r') as f:
        channelss = json.load(f)

    channelss[str(ctx.guild.id)] = int(channels.id)

    with open('suggestionchannels.json','w') as f:
        json.dump(channelss,f,indent=4)

    await ctx.respond(f"set your suggestion channel to {channels}")     
#Start Fun Commands(End of todo.) 
@bot.slash_command(description="Flips A Coin")
@commands.guild_only()
@commands.cooldown(1, 500, commands.BucketType.user) 
async def coinflip(ctx): 
    lst = ('https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/US_One_Cent_Obv.png/220px-US_One_Cent_Obv.png','https://www.pngitem.com/pimgs/m/61-613669_one-clipart-cent-penny-head-and-tail-hd.png')
    embed = discord.Embed(
      title=f"{ctx.author} Fliped A Coin",   
      description=f"And It Landed On!",
      colour=0xFF0000
      )
    embed.set_image(url=random.choice(lst))
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
@coinflip.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("You cant flip a coin that fast! 30s")
    else:
        raise error  
    
@bot.command(name="8ball", description="Uses The 8ball")
@commands.guild_only()
async def _8ball(ctx, question):
    lst = ('Maybe', 'Yes', 'It Seems So', 'As I See It, Yes.', 'Probably Not', 'Not Today, No.', 'Maybe Tommorow', 'Hell Yeah', 'Im not Sure', 'Totally')
    embed = discord.Embed(
     title=f"🎱 {question}",
     description=random.choice(lst),
     colour=0xFF0000
    )
    embed.set_footer(text=f"Asked By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)

@bot.slash_command(description="Sends A Suggestion to the specified channel!")
@commands.guild_only()
@commands.cooldown(1, 3600, commands.BucketType.user) 
async def suggest(ctx, content):
    with open('suggestionchannels.json', 'r') as f:
        channelss = json.load(f)


    channel_log = ctx.guild.get_channel(channelss[str(ctx.guild.id)])
    embed = discord.Embed(
     title="A New Suggestion",
     description=f"From {ctx.channel.mention}",
     colour=0xFF0000
    )
    embed.set_author(name=f"{ctx.author.mention}", icon_url=f"{ctx.author.avatar.url}")
    embed.add_field(name=f"{ctx.author.mention} Suggests", value=(content))
    embed.timestamp = datetime.datetime.now()
    message = await channel_log.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    embed = discord.Embed(
    title="A New Suggestion",
     description=f"This comes from {ctx.guild.name}",
     colour=0xFF0000
    )
    embed.set_author(name=f"{ctx.author.mention}", icon_url=f"{ctx.author.avatar.url}")
    embed.add_field(name=f"{ctx.author.mention} Suggests", value=(content))
    embed.set_footer(text="This is the suggestion you just sent!")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed, ephemeral=True)
    
@bot.slash_command(name="mainsuggest", description="Sends A Suggestion To The Offical Discord Server!")
@commands.guild_only()
@commands.cooldown(1, 3600, commands.BucketType.user) 
async def dsuggest(ctx, content):
    channel = bot.get_channel(1010855363597303808)
    embed = discord.Embed(
     title="A New Suggestion",
     description=f"This comes from {ctx.guild.name}",
     colour=0xFF0000
    )
    embed.set_author(name=f"{ctx.author.mention}", icon_url=f"{ctx.author.avatar.url}")
    embed.add_field(name=f"{ctx.author.mention} Suggests", value=(content))
    embed.timestamp = datetime.datetime.now()
    message = await channel.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    embed = discord.Embed(
    title="A New Suggestion",
     description=f"This comes from {ctx.guild.name}",
     colour=0xFF0000
    )
    embed.set_author(name=f"{ctx.author.mention}", icon_url=f"{ctx.author.avatar.url}")
    embed.add_field(name=f"{ctx.author.name} Suggests", value=(content))
    embed.set_footer(text="This is the suggestion you just sent!")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed, ephemeral=True)    
@dsuggest.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("You can only send one suggestion a hour!")
    else:
        raise error   
@suggest.error
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("You can only send one suggestion a hour!")
    else:
        raise error    

@bot.command(description="How Big Is Ur PP")
@commands.guild_only()
async def howbig(ctx):
    lst = ('1 Inch, Small','2 inches','3 inches','4 inches','5 inches, Average','6 inches what women perfer 😉','7 inches', '8 inches','9 inches','10 inches, Damn. 😏')
    embed = discord.Embed(
     title=f"Your PP Is!",
     description=random.choice(lst),
     colour=0xFF0000
    )
    embed.set_footer(text=f"Asked By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)    

@bot.command(description="rolls a dice")
@commands.guild_only()
async def diceroll(ctx):
    lst = ('https://i.gyazo.com/b25f7e7bfd052065ce8f8edba23c4ceb.png','https://i.gyazo.com/6e9ded01227fcf84ef72a6b2cc323b79.png','https://i.gyazo.com/6e9ded01227fcf84ef72a6b2cc323b79.png','https://i.gyazo.com/a40e63876040f9e090c2b867efa0c1a7.png', 'https://i.gyazo.com/8925363ba558f96cb2d1c8a65b17bc53.png','https://i.gyazo.com/178cfc0543827a772fab1cfd993eed54.png')
    embed = discord.Embed(
     title=f"{ctx.author} Rolled The Dice",
     description="🎲And it landed on!",
     colour=0xFF0000
    )
    embed.set_image(url=random.choice(lst))
    embed.set_footer(text=f"Rolled By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)    
    
@bot.command(description="make a embed")
@commands.guild_only()
async def embedcreate(ctx, title, description, url, fieldname, fieldvalue, field2, fieldv2):
    embed = discord.Embed(
      title=(title),
      description=(description),
      color=0xFF0000
      )
    embed.set_image(url=(url))
    embed.add_field(name=(fieldname), value=(fieldvalue))
    embed.add_field(name=(field2), value=(fieldv2))
    await ctx.respond(embed=embed)

@bot.command(description="How much of a simp are you?")
@commands.guild_only()
async def simpdetector(ctx, member: discord.Member):
    lst =('5','10','15','20','25','30','35','40','45','50','55','60','65','70','75','80','85','90','95','100',)
    embed = discord.Embed(
     title=f"Simp Detected",
     description=f"**{ctx.author}** Is Using Simp Detection On **{member.mention}**",
     colour=0xFF0000
    )
    embed.add_field(name="Results", value=f"**{member.mention}** is **{random.choice(lst)}%** Simp")
    embed.set_footer(text=f"Requested By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)

@bot.command(description="Get your profile picture!")
async def av(ctx):
    embed = discord.Embed(
     title="Someone Say Pfp?",
     description=f"{ctx.author.mention}'s pfp",
     color=0xFF0000
    )
    embed.set_image(url=ctx.author.avatar.url)
    await ctx.respond(embed=embed)
    
@bot.command()
@commands.guild_only()
async def botinfo(ctx):
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    embed = discord.Embed(
     title="Here you go!",
     description="The Bot's Info",
     colour=0xFF0000
    )
    embed.set_thumbnail(url="https://i.gyazo.com/ae6a40f3407f80097e78115d8538f7ab.jpg")
    embed.add_field(name="Owner", value="Slim Beatbox#3032")
    embed.add_field(name="Total Server's", value=f"{len(bot.guilds)}/100")
    embed.add_field(name="Total Member's Watching", value=f"{members}")
    embed.add_field(name="Language", value="[Python](https://en.wikipedia.org/wiki/Python_(programming_language)")
    embed.add_field(name="Language Wrapper", value="[Pycord](https://guide.pycord.dev/introduction)")
    embed.add_field(name="Creation Date", value="Mon, Aug 08, 2022 @ 10:26 PM")
    embed.add_field(name="Host", value=host.mention)
    embed.set_footer(text=f"Requested By {ctx.author}")
    embed.timestamp = datetime.datetime.now()
    starttime = datetime.datetime.now()  
    await ctx.respond(embed=embed)

@bot.command(description="Get all roles of the server, role amount cannot be over 42")
async def dsroles(ctx):
    embed = discord.Embed(
     title="Here you go",
     description="All the roles",
     colour=0xFF0000
    )
    embed.add_field(name="Roles", value=f"{' '.join([role.mention for role in ctx.guild.roles if role.name != '@everyone'])}")
    await ctx.respond(embed=embed)
#Message Count Leaderboard                                               
@bot.listen()
@commands.guild_only()
async def on_message(message):
    if message.author is message.author.bot: 
        print("Bot Message")
    else:
        with open('messages.json','r') as f:
            global message_count
            message_count = json.load(f)
            if message.guild.name not in message_count:
                message_count[message.guild.name] = {}
            try:
                message_count[message.guild.name][message.author.name] += 1
            except KeyError:
                message_count[message.guild.name][message.author.name] = 1
        with open('messages.json','w') as f:
                json.dump(message_count,f,indent=4)   
                
@bot.command(description="Total message count for you server!")
@commands.cooldown(1, 20, commands.BucketType.user) 
@commands.guild_only()
async def leaderboard(ctx):
	listValues = []
	sortedList = []

	embed = discord.Embed(
			 title="Leadboard",
			 description=f"{ctx.guild.name}, Do {dleaderboard.mention} to see deleted message count",
			 color=0xFF000
			)
	
	with open('messages.json') as file:
		data = json.load(file)
		listValues = new_list = list(map(list, data[f"{ctx.guild.name}"].items()))
		
	sortedList = sorted(listValues, key=itemgetter(1), reverse=True)
	strToPrint = ""
	for item in sortedList : 
		strToPrint = strToPrint +"\n"+ item[0] +" : "+str(item[1])  
	embed.add_field(name="━━━━━━━━━━━━Total Messages Sent!━━━━━━━━━━━━━", value=f"**{strToPrint}**" )
	embed.set_footer(text="If you feel your message's are not being counted, please get the server owner to send me a dm!")
	await ctx.respond(embed=embed)
#Deleted Message Count(Message Count End)
@bot.listen()
@commands.guild_only()
async def on_message_delete(message):
    with open('deleted_msgs.json','r') as f:
            global message_count
            message_count = json.load(f)
            if message.guild.name not in message_count:
                message_count[message.guild.name] = {}
            try:
                message_count[message.guild.name][message.author.name] += 1
            except KeyError:
                message_count[message.guild.name][message.author.name] = 1
            with open('deleted_msgs.json','w') as f:
                json.dump(message_count,f,indent=4)   

@bot.command(description="Deleted message count for your server!")
@commands.cooldown(1, 20, commands.BucketType.user) 
@commands.guild_only()
async def dleaderboard(ctx):
	listValues = []
	sortedList = []

	embed = discord.Embed(
			 title="Leadboard",
			 description=f"{ctx.guild.name}, **Deleted Messages Since The Bot Joined!**",
			 color=0xFF000
			)
	
	with open('deleted_msgs.json') as file:
		data = json.load(file)
		listValues = new_list = list(map(list, data[f"{ctx.guild.name}"].items()))
		
	sortedList = sorted(listValues, key=itemgetter(1), reverse=True)
	strToPrint = ""
	for item in sortedList : 
		strToPrint = strToPrint +"\n"+ item[0] +" : "+str(item[1])  
	embed.add_field(name="━━━━━━━━━━━Total Messages Deleted!━━━━━━━━━━━", value=f"**{strToPrint}**" )
	embed.set_footer(text="If you feel your message's are not being counted, please get the server owner to send me a dm!")
	await ctx.respond(embed=embed)          

@bot.listen()
async def on_message(message):
    role = discord.utils.get(message.guild.roles, name="Bumpies")
    if message.guild.id == (842791991008165898):
        if message.author.id == (302050872383242240):
                embed = discord.Embed(
                 title="Bumpity Bump!",
                 description=f"Thanks for bumping {message.guild.name}! I shall remind you in 2 hours.",
                 color=0x24b8b8
                )
                embed.set_footer(text="Remember, you must have a role called 'Bumpies' or you wont be pinged!")
                await message.channel.send(embed=embed)
                await asyncio.sleep(7200)
                await message.channel.send(f"Hey Broski, It's Bumpin Time! {role.mention}")

@bot.command(pass_context=True)
async def runtime(ctx):
    now = datetime.datetime.now()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    embed = discord.Embed(
    title="Runtime",
    description="Running for {}d {}h {}m {}s".format(elapsed.days, hours, minutes, seconds),
    color=0xFF0000
    )
    embed.set_footer(text="If You Were Wondering")
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed)
starttime = datetime.datetime.now() 
