import discord
from discord.ext import commands
import aiohttp
import Fluffy

class events(commands.Cog):
    def __init__(self, client):
        self.client = client  

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Is Ready")
        
    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        if guild.member_count < 70:
            await guild.leave()
        else:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=Fluffy.guild_join,session=session)
                embed = discord.Embed(title="Joined A Guild", description=f"**ID:** {guild.id}\n**Name:** {guild.name}\n**MemberCount:** {len(guild.members)}\n**Created:** <t:{int(guild.created_at.timestamp())}:R>", color=0x2b2d31)    
                await webhook.send(embed=embed)       
            
    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: discord.Guild):
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=Fluffy.guild_leave,session=session)
                embed = discord.Embed(title="Left A Guild", description=f"**ID:** {guild.id}\n**Name:** {guild.name}\n**MemberCount:** {len(guild.members)}\n**Created:** <t:{int(guild.created_at.timestamp())}:R>", color=0x2b2d31)
                await webhook.send(embed=embed)       


    @commands.Cog.listener()
    async def on_message(self, message, ctx):
        cur = self.con.cursor()
        cur.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (ctx.guild.id,))
        server_prefix = cur.fetchone()
        prefix = server_prefix[0] if server_prefix else "&"
        if message.content == self.client.user.mention:
            embed = discord.Embed(
                description=f"Hey {message.author.mention}\n My prefix here is `{prefix}` \n Server ID: `{message.guild.id}` \n \n Type `&help` To Get The Command List",
                color=discord.Color.random()
            )
            embed.set_thumbnail(url=message.author.avatar)
            embed.set_footer(
                text="Managed By Fluffy Dev",
                icon_url="https://cdn.discordapp.com/attachments/1197078320794304532/1199684377009983528/1ce597c0e0ec818e.jpeg?ex=65c37024&is=65b0fb24&hm=a5b79046e047c4e05bc9a4854e6c9a7f5fec67e2f25a56cc3d5c933687f8d58f&"
            )
            embed.set_author(name=message.author.name,
                             icon_url=message.author.display_avatar.url)

            # Create "Support" button with link "https://discord.gg/HsHqdXbXkn"
            support_button = discord.ui.Button(label="Support", url="https://discord.gg/RQ3qKDq5gk")

            
            Invite_button = discord.ui.Button(label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=1197167504376725698&permissions=8&scope=bot")

            
            embed.color = self.color

            
            view = discord.ui.View().add_item(Invite_button).add_item(support_button)

            
            await message.reply(embed=embed, view=view, mention_author=False)








async def setup(client):
    await client.add_cog(events(client))        