import discord
from discord.ext import commands, tasks
import datetime
import random

intents = discord.Intents.default()
intents.members = True

#command prefix
clay = commands.Bot(command_prefix='_', intents=intents)


#warmup
@clay.event
async def on_ready():
	print('ClaY is running')
	await clay.change_presence(activity=discord.Game("কি আছে জীবনে 🤷‍♂️"))

	
#bot icon image
bot_icon = 'https://cdn.discordapp.com/avatars/777850935477010454/50532b2fccb678a2816e8a7abc9f0ff4.png'
#default channel
#d_channel = 703531219899383851
d_channel = 777913338268483614 #bot test channel

#wecoming new member
@clay.event
async def on_member_join(member):  
    channel = clay.get_channel(d_channel)
    #print(channel)
    embed = discord.Embed(title= 'Welcome', description=f'Hola {member.mention} 👋 \n Welcome to Upward Gravity 👾', color=0x009411)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    if channel != None:
        await channel.send(embed=embed)
    else:
        for guild in clay.guilds:
            for channels in guild.text_channels:
                #text_channel_list.append(channel)
                if channels == 'general':
                    await channels.send(embed=embed)
    # print(text_channel_list[0])
    #Welcome DM
    embed1 = discord.Embed(title="Welcome", description="Welcome to Updward Gravity. Feel free to join then channels and communicate with other members.", color=0x0e920c)
    embed1.set_thumbnail(url=member.guild.icon_url)
    embed1.set_footer(text="Checkout the source code of this bot at https://github.com/FHShubho/ClaY_the_bot")
    await member.send(embed=embed1)


#farewell member
@clay.event
async def on_member_remove(member):
    channel = clay.get_channel(d_channel)
    embed = discord.Embed(title= 'Farewell', description=f'We had to let go {member.mention} \n Goodbye 👋 ', color=0x009411)
    if channel != None:
        await channel.send(embed=embed)
    else:
        for guild in clay.guilds:
            for channels in guild.text_channels:
                #text_channel_list.append(channel)
                if channels == 'general':
                    await channels.send(embed=embed)


#reply latency
@clay.command()
async def ping(ctx):
    await ctx.send(f'🌐 {round (clay.latency * 1000)}ms ')


#userinfo
@clay.command()
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    else:
        member = member
    roles = []
    
    for role in member.roles:
        roles.append(role.name)

    embed = discord.Embed(title = 'ℹ️ User Info', colour = discord.Colour.green(), timestamp= ctx.message.created_at)
    embed.set_author(name=member.display_name)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'info requested by - {ctx.author.name}', icon_url=ctx.author.avatar_url)

    embed.add_field(name='Orignal Name', value=member.name, inline=False)
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Joined Discord', value=member.created_at.strftime("%a %#d %B %Y \n %I:%M %p UTC"))
    embed.add_field(name='Joined Server', value=member.joined_at.strftime("%a %#d %B %Y \n %I:%M %p UTC"))
    embed.add_field(name='Roles', value=roles, inline=False)
    embed.add_field(name='Top Role', value=member.top_role)
    await ctx.send(embed=embed)


#kick
@clay.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason=None):
    #kick DM
    embed1 = discord.Embed(title="⚽ Kick Notice", description=f"You have been kicked from {member.guild.name}", color=0x0e920c)
    embed1.set_thumbnail(url=member.guild.icon_url)
    embed1.add_field(name='Reason', value=reason)
    await member.send(embed=embed1)
    #kick message to server
    embed = discord.Embed(title= '⚽ Flying Kick', description=f'{member.mention} has been kicked👾', color=0x009411, timestamp= ctx.message.created_at)
    embed.add_field(name='Reason', value=reason)
    embed.set_footer(text=f'Kicked by - {ctx.author.name}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    #kicked
    await member.kick(reason=reason)


#ban
@clay.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    #kick message to server
    embed = discord.Embed(title= '🚫 Banned', description=f'{member.mention} has been Banned👾', color=0x009411, timestamp= ctx.message.created_at)
    embed.add_field(name='Reason', value=reason)
    embed.set_footer(text=f'Ban Hammered by - {ctx.author.name}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    #kick DM
    embed1 = discord.Embed(title="🚫 Ban Notice", description=f"You have been banned from {member.guild.name}", color=0x0e920c)
    embed1.set_thumbnail(url=member.guild.icon_url)
    embed1.add_field(name='Reason', value=reason)
    await member.send(embed=embed1)
    #banned
    await member.ban(reason=reason)


#unban
@clay.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        print(user.name)
        print(user.discriminator)
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user, reason=None)
            #unban message to server
            embed = discord.Embed(title= '⭕ Unbanned', description=f'{user.mention} has been Unbanned👾', color=0x009411, timestamp= ctx.message.created_at)
            embed.set_footer(text=f'Unbanned by - {ctx.author.name}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return


#server info
@clay.command()
async def serverinfo(ctx):
    embed = discord.Embed(title = '📜 Server Info', colour = discord.Colour.green(), timestamp= ctx.message.created_at)
    embed.set_author(name=ctx.guild.name)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f'info requested by - {ctx.author.name}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='Server ID', value=ctx.guild.id, inline=False)
    embed.add_field(name='Server Owner', value=ctx.guild.owner)
    embed.add_field(name='Server Created', value=ctx.guild.created_at.strftime("%a %#d %B %Y \n %I:%M %p UTC"))
    embed.add_field(name='Server Region', value=ctx.guild.region)
    embed.add_field(name='AFK Channel', value=ctx.guild.afk_channel)

    text_count = len(ctx.guild.text_channels)
    embed.add_field(name='Text Channels', value=text_count)

    voice_count = len(ctx.guild.voice_channels)
    embed.add_field(name='Voice Channels', value=voice_count)

    embed.add_field(name='Total Members', value=ctx.guild.member_count)

    all_roles = len(ctx.guild.roles)
    embed.add_field(name='Total Roles', value=all_roles)
    
    current_time = datetime.datetime.now()
    created_time = ctx.guild.created_at
    elapsed = current_time - created_time
    embed.add_field(name='Server age', value=elapsed)

    await ctx.send(embed=embed)


#bot info
@clay.command()
async def botinfo(ctx):
    embed = discord.Embed(title = '🤖 ClaY the BOT', description = 'Bot information', colour = discord.Colour.green())
    embed.set_thumbnail(url=bot_icon)
    embed.set_footer(text='GitHub Repo: https://github.com/FHShubho/ClaY_the_bot')

    server_count = len(clay.guilds)
    embed.add_field(name='Server Count', value=server_count, inline=False)

    channel_count = len(set(clay.get_all_channels()))
    embed.add_field(name='Channels visible to bot', value=channel_count, inline=False)

    bot_created = datetime.datetime(2020, 11, 16)
    current_time = datetime.datetime.now()
    bot_age = current_time - bot_created
    embed.add_field(name='Bot Age', value=bot_age, inline=False)

    await ctx.send(embed=embed)


#set nickname
@clay.command()
@commands.has_permissions(manage_nicknames = True)
async def setnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)

    embed = discord.Embed(title= 'Nickname Changed', description=f'{member.name} is now {member.mention} 👾', color=0x009411, timestamp= ctx.message.created_at)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Nickname changed by - {ctx.author.name}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


#default help command removed
clay.remove_command('help')


#command list
@clay.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title = '📢Command list', description = 'Currently available Commands', colour = discord.Colour.green())
    embed.set_thumbnail(url=bot_icon)
    embed.set_footer(text='More information at https://github.com/FHShubho/ClaY_the_bot', icon_url=bot_icon)

    embed.add_field(name='_ping', value='☑️ Replies latency time', inline=False)
    embed.add_field(name='_help', value='☑️ Replies available command list', inline=False)
    embed.add_field(name='_features', value='☑️ Replies current features of the BOT', inline=False)
    embed.add_field(name='_userinfo', value='☑️ Replies with the information about message author', inline=False)
    embed.add_field(name='_userinfo @user', value='☑️ Replies with the information about @user', inline=False)
    embed.add_field(name='_serverinfo', value='☑️ Replies with the information about the server', inline=False)
    embed.add_field(name='_botinfo', value='☑️ Replies with the information about the bot', inline=False)
    embed.add_field(name='_kick @member', value='☑️ Kicks the member out of server with a DM (Requires kick member permission)', inline=False)
    embed.add_field(name='_kick @member reason', value='☑️ Kicks the member out of server and notifies with a reason (Requires kick member permission)', inline=False)
    embed.add_field(name='_ban @member', value='☑️ Bans the member from server with a DM (Requires ban member permission)', inline=False)
    embed.add_field(name='_ban @member reason', value='☑️ Bans the member from server and notifies with a reason (Requires ban member permission)', inline=False)
    embed.add_field(name='_unban user#discriminator', value='☑️ Unbans the banned user in the server(Requires administritive permission)', inline=False)
    embed.add_field(name='_setnick @member nickname', value='☑️ Changes nickname of the member (Requires manage nickname permission)', inline=False)

    await ctx.send(embed=embed)


#feature list
@clay.command(pass_context=True)
async def features(ctx):
    embed = discord.Embed(
        title = '🤖Bot Features',
        description = '☑️ Welcome Message \n ☑️ Welcome DM and Farewell Message \n ☑️ Latency \n ☑️ User, Server and Bot Information \n ☑️ Kick, ban and unban members \n ☑️ Change nicknames \n' ,
        colour = discord.Colour.green(),
        url = 'https://github.com/FHShubho/ClaY_the_bot')
    embed.set_author(name='ClaY th BOT', icon_url=bot_icon)
    embed.add_field(name='GitHub Repo', value='🔗https://github.com/FHShubho/ClaY_the_bot', inline=False)

    await ctx.send(embed=embed)


#Motivating abrar to come back to valorant with random messages
barta = open('barta.txt', 'r').readlines()

@clay.event
async def on_message(message):
    lekhok = message.author.id
    if lekhok == 409442871775854595:
        temp = random.randint(0,3)
        if temp == 2:
            temp_number = random.randint(0, 10)
            monu = barta[temp_number]
            channel = message.channel
            author = message.author
            await channel.send(f'{author.mention} ' + monu)


#Error message
@clay.event
async def on_command_error(ctx, error):
    await ctx.send(f'❌Error: ({error})')


#fetching the secret token
token = open('token.txt','r').readline()

clay.run(token)
