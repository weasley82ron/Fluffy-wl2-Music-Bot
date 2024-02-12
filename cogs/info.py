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
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):
        guilds = ctx.bot.guilds
        num_guilds = len(guilds)
        num_users = sum(guild.member_count for guild in guilds)
        num_commands = 70

        current_time = datetime.datetime.now()
        uptime = current_time - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_str = f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"

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









    @commands.command(aliases=['up'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx):
        current_time = datetime.datetime.now()
        uptime = current_time - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_str = f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
        embed = discord.Embed(description=f"Uptime: {uptime_str}",colour=self.color)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
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

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        view = MyView(Fluffy.bot_link, Fluffy.support_link)
        embed = discord.Embed(
            title="Fluffy Invite",
            description="**Invite me. Need Support?** \n **Join Support Server Using The Button Below -**",
            color=self.color
        )
        await ctx.reply(embed=embed, mention_author=False, view=view)

  
    @commands.command()
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