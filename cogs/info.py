import discord
import asyncio
import sqlite3
import datetime
from discord.ext import commands
import Fluffy
from discord.ui import Button, View
import psutil

class MyButton(Button):
  def __init__(self, label, url):
      super().__init__(style=discord.ButtonStyle.link, label=label, url=url)

class MyView(View):
  def __init__(self, invite_url, support_url):
      super().__init__()
      self.add_item(MyButton("Invite", invite_url))
      self.add_item(MyButton("Support", support_url))







class info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.start_time = datetime.datetime.now()
        self.color = Fluffy.color
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info Is Ready")   
    
    @commands.command(aliases=['bi'], help="Shows The Stats Of The Bot", usage = "stats")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):
        guilds = ctx.bot.guilds
        num_guilds = len(guilds)
        num_users = sum(guild.member_count for guild in guilds)
        num_commands = 45

        current_time = datetime.datetime.now()
        uptime = current_time - self.start_time

        # Convert uptime to seconds
        total_seconds = int(uptime.total_seconds())

        # Format uptime as a Unix timestamp
        uptime_timestamp = int(self.start_time.timestamp())

        # Format uptime as a timestamp string
        uptime_str = f"<t:{uptime_timestamp}>"
        self.cpu_percent = psutil.cpu_percent()
        self.ram_info = psutil.virtual_memory()

        embed = discord.Embed(
            title="__Stats__",
            description=f"**Total Servers:** {num_guilds}\n"
                        f"**Total Users:** {num_users}\n"
                        f"**Total Commands:** {num_commands}\n"
                        f"**Uptime:** {uptime_str}\n"
                        f"**Shards:** AutoSharded\n"
                        f"**CPU Usage:** {self.cpu_percent}%\n",
            color=self.color
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="Powered By Fluffy Services", icon_url=Fluffy.icon)
        await ctx.reply(embed=embed, mention_author=False, view=MyView(Fluffy.bot_link, Fluffy.support_link))

    @commands.command(invoke_without_command=True,
                help="Clears the messages",
                usage="purge <amount>", aliases=['clean'])
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        deleted = await ctx.channel.purge(limit=amount + 1)
        return await ctx.send(
            f"** Deleted {len(deleted)-1} message(s)**"
        )









    @commands.command(aliases=['up'], help="Check The Bot Uptime", usage = "uptime")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx):
        current_time = datetime.datetime.now()
        uptime = current_time - self.start_time

        # Convert uptime to seconds
        total_seconds = int(uptime.total_seconds())

        # Format uptime as a Unix timestamp
        uptime_timestamp = int(self.start_time.timestamp())

        # Format uptime as a timestamp string
        uptime_str = f"<t:{uptime_timestamp}>"
        embed = discord.Embed(description=f"I am online from {uptime_str}",colour=self.color)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['latency'], help="See The Realtime Latency Of The Bot", usage = "ping")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        # Get latency from the client object
        latency = round(self.client.latency * 1000)

        embed = discord.Embed(
            color=self.color
        )
        embed.set_author(name=f"{latency}ms Pong! ", icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text="Fluffy Services", icon_url=Fluffy.icon)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['inv'], help="Shows Bot's Links", usage = "invite")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        view = MyView(Fluffy.bot_link, Fluffy.support_link)
        embed = discord.Embed(
            title="Fluffy Invite",
            description="**Invite me. Need Support?** \n **Join Support Server Using The Button Below -**",
            color=self.color
        )
        await ctx.reply(embed=embed, mention_author=False, view=view)

  
    @commands.command(aliases=['sup'], help="Shows Bot's Links", usage = "support")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support(self, ctx):
      view = MyView(Fluffy.bot_link, Fluffy.support_link)
      embed = discord.Embed(
            title="Support",
            description=f"**Need Support?** \n **Join Support Server Using The Button Below -**",
            color=self.color
      )
      await ctx.reply(embed=embed, mention_author=False, view=view)






async def setup(client):
    await client.add_cog(info(client))