import discord
from discord.ext import commands
import os 
import Fluffy
from typing import Optional, Union
from emojis import tick, cross
from discord.utils import get
from afks import afks

def remove(afk):
    if "" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = Fluffy.color

        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility Is Ready")  

    @commands.command(name='avatar', aliases=['av'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: Optional[Union[discord.Member, discord.User]] = None):
     try:
      if member is None or member == "":
        member = ctx.author
      user = await self.client.fetch_user(member.id)
      webp = user.avatar.replace(format='webp')
      jpg = user.avatar.replace(format='jpg')
      png = user.avatar.replace(format='png')
      embed = discord.Embed(
        color=self.color,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not user.avatar.is_animated()
        else f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({user.avatar.replace(format='gif')})"
    )
      embed.set_author(name=f"{member}",
                     icon_url=member.avatar.url
                     if member.avatar else member.default_avatar.url)
      embed.set_image(url=user.avatar.url)
      embed.set_footer(text=f"Requested By {ctx.author}",
                     icon_url=ctx.author.avatar.url
                     if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=embed)
     except Exception as e:
       await ctx.send(e)



    @commands.group(name="banner", invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def banner(self, ctx):
      try:
        embed = discord.Embed(title="Banner", color=self.color)
        embed.description = """
`banner user` - **Shows The Banner Of Mentioned User.**\n
`banner server` - **Shows The Banner Of The Server.**
"""  
        await ctx.send(embed=embed)
      except Exception as e:
         print(e)

    @banner.command(name="server")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server(self, ctx):
     if not ctx.guild.banner:
      await ctx.reply(f"**{cross} | This server does not have a banner.**")
     else:
      webp = ctx.guild.banner.replace(format='webp')
      jpg = ctx.guild.banner.replace(format='jpg')
      png = ctx.guild.banner.replace(format='png')
      embed = discord.Embed(
        color=self.color,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not ctx.guild.banner.is_animated() else
        f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({ctx.guild.banner.replace(format='gif')})"
      )
      embed.set_image(url=ctx.guild.banner)
      embed.set_author(name=ctx.guild.name,
                       icon_url=ctx.guild.icon.url
                       if ctx.guild.icon else ctx.guild.default_icon.url)
      embed.set_footer(text=f"Requested By {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)
      await ctx.reply(embed=embed)


    @banner.command(name="user")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.guild_only()
    async def _user(self,
                  ctx,
                  member: Optional[Union[discord.Member,
                                         discord.User]] = None):
     if member == None or member == "":
      member = ctx.author
     bannerUser = await self.client.fetch_user(member.id)
     if not bannerUser.banner:
      await ctx.reply("{} **|** {} **does not have a banner.**".format(cross, member))
     else:
      webp = bannerUser.banner.replace(format='webp')
      jpg = bannerUser.banner.replace(format='jpg')
      png = bannerUser.banner.replace(format='png')
      embed = discord.Embed(
        color=self.color,
        description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
        if not bannerUser.banner.is_animated() else
        f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({bannerUser.banner.replace(format='gif')})"
      )
      embed.set_author(name=f"{member}",
                       icon_url=member.avatar.url
                       if member.avatar else member.default_avatar.url)
      embed.set_image(url=bannerUser.banner)
      embed.set_footer(text=f"**Requested By** {ctx.author}",
                       icon_url=ctx.author.avatar.url
                       if ctx.author.avatar else ctx.author.default_avatar.url)

      await ctx.send(embed=embed)




    @commands.command(aliases=['mc', 'member'])
    async def members(self, ctx):
      guild = ctx.guild
      embed = discord.Embed()
      embed.add_field(name=f"Member Count", value=f" **{len(guild.members)}**")
      await ctx.reply(embed=embed)


    @commands.command()
    async def afk(self, ctx, *, reason="**Am I AFK?**"):
        member = ctx.author
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick = f" {member.display_name}")
            except:
                pass
        try:
         afks[member.id] = reason
        except Exception as e:
            await ctx.send(e)
        await ctx.send(embed=discord.Embed(description=f"Your AFK is now set to: **{reason}**", color=self.color))
 
    @commands.Cog.listener()
    async def on_message(self, message):
            if message.author.id in afks.keys():
                    afks.pop(message.author.id)
                    await message.channel.send(embed=discord.Embed(description=f"{message.author.mention}, I removed your AFK. ", color=self.color))
                    return
            for id, reason in afks.items():
                        member = get(message.guild.members, id = id)
                        if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                                       await message.reply(embed=discord.Embed(description=f"**{member.mention}** is AFK: {reason}", color=self.color))
       


       



async def setup(client):
    await client.add_cog(Utility(client))