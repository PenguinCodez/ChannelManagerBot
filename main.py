import discord
import os
import keep_alive
from itertools import cycle
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='cm!', description='A bot that manages your channels.')
intents = discord.Intents.all()
status = cycle(['in channels', 'with channels', 'hide and seek in channels'])

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(title='NightFlame Help Menu', description=page, color=0x16286f)
            await destination.send(embed=emby)

client.help_command = MyNewHelp()

@client.event
async def on_ready():
    change_status.start()
    print('i am a channel bot.')

@client.command(aliases=['n'], description='Change the name of a text channel.')
@commands.has_permissions(manage_channels=True)
async def name(ctx, channel: discord.TextChannel, *, new_name):
    await channel.edit(name=new_name)
    await ctx.send(f'{channel} has been successfully changed to {new_name}')

@name.error
async def channelname_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify a channel and/or a new name.')

@client.command(description='Hide a channel to prevent people from reading messages.')
@commands.has_permissions(manage_channels=True)
async def hide(self, ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.read_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel hidden.')

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(self, ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel unlocked.')

@commands.command(description='Use this command on a channel to allow people to read messages.')
@commands.has_permissions(manage_channels=True)
async def show(self, ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.read_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel is now viewable to everyone.')

@client.command(description='Lock a channel to prevent people from sending messages.')
@commands.has_permissions(manage_channels=True)
async def lock(self, ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')

@client.command(aliases=['rl'], description='Lock a channel to prevent __a role__ from sending messages.')
@commands.has_permissions(manage_channels=True)
async def rolelock(self, ctx, role : discord.Role, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    perms = channel
    await channel.set_permissions(role, send_messages=False)
    await ctx.send(f'Channel {channel} locked for {role.name}.')

@client.command(aliases=['rul'], description='Lock a channel to prevent __a role__ from sending messages.')
@commands.has_permissions(manage_channels=True)
async def roleunlock(self, ctx, role : discord.Role, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    perms = channel
    await channel.set_permissions(role, send_messages=True)
    await ctx.send(f'Channel {channel} unlocked for {role.name}.')

@client.command(aliases=['rs'])
@commands.has_permissions(manage_channels=True)
async def roleshow(self, ctx, role : discord.Role, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    perms = channel
    await channel.set_permissions(role, read_messages=True)
    await ctx.send(f'Channel {channel} is now viewable to {role.name}.')

@client.command(aliases=['rh'])
@commands.has_permissions(manage_channels=True)
async def rolehide(self, ctx, role : discord.Role, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    perms = channel
    await channel.set_permissions(role, read_messages=False)
    await ctx.send(f'Channel {channel} hidden for {role.name}.')

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

keep_alive.keep_alive()

client.run(os.getenv("TOKEN"))