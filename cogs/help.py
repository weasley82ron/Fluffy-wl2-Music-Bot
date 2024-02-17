import discord
import asyncio
import sqlite3
from discord.ext import commands
import Fluffy
from emojis import *

class MenuView(discord.ui.View):
    def __init__(self, author, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None  
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()        

    @discord.ui.select(placeholder="Fluffy Dev", options=[
        discord.SelectOption(label="Music", value="music"),
        discord.SelectOption(label="Utility", value="utility"),
        discord.SelectOption(label="Filter", value="filter"),
        discord.SelectOption(label="Info", value="info"),
        ])
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("Sorry Bro, This is not your interaction.", ephemeral=True)
                return
            selected_values = select.values
            if selected_values and "music" in selected_values:
                embed = discord.Embed(colour=Fluffy.color, description="`Play`, `Pause`, `Resume`, `Stop`, `Queue`, `Volume`, `Skip`, `ClearQueue`, `DefaultVolume`, `Move`, `Join`, `Leave`, `NowPlaying`, `Forward`, `Rewind`, `Seek`, `Remove`")
                embed.set_author(name="Music Commands", icon_url=Fluffy.icon)
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "utility" in selected_values:
                embed = discord.Embed(colour=Fluffy.color, description="`Avatar`, `Banner`, `MemberCount`, `Afk`")
                embed.set_author(name="Utility Commands", icon_url=Fluffy.icon)
                await interaction.response.edit_message(embed=embed, view=self)                
            elif selected_values and "filter" in selected_values:
                embed = discord.Embed(colour=Fluffy.color, description="`Vaporwave`, `Lofi`, `8d`, `Slowmo`, `BassBoost`, `China`, `Chipmunk`, `DarthVader`, `Demon`, `Funny`, `Karoke`, `NightCore`, `Pop`, `Soft`, `TrebleBass`, `Tremolo`, `Alien`, `Reset`")
                embed.set_author(name="Filter Commands", icon_url=Fluffy.icon)
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "info" in selected_values:
                embed = discord.Embed(colour=Fluffy.color, description="`Ping`, `Purge`, `Uptime`, `Invite`, `Support`, `Stats`, `Setpreifx`, `Help`")
                embed.set_author(name="Info Commands", icon_url=Fluffy.icon)
                await interaction.response.edit_message(embed=embed, view=self)
            
            select.placeholder = None 
        except Exception as e:
            print(f"An error occurred: {e}")
            raise   
            
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()          

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Is Ready")    

    @commands.command(aliases=['h'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *, query=None):
        cur = self.con.cursor()
        cur.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (ctx.guild.id,))
        server_prefix = cur.fetchone()
        prefix = server_prefix[0] if server_prefix else "&"
        view = MenuView(ctx.author)
        embed = discord.Embed(colour=Fluffy.color, description=f"{dot} My prefix for this server is `{prefix}`\n{dot} Total Commands `45`\n{dot} [**Fluffy**]({Fluffy.bot_link}) | [**Support**]({Fluffy.support_link})\n{dot} Thanks for using Fluffy")
        
        embed.add_field(name="Music", value='`Play`, `Pause`, `Resume`, `Stop`, `Queue`, `Volume`, `Skip`, `ClearQueue`, `DefaultVolume`, `Move`, `Join`, `Leave`, `NowPlaying`, `Forward`, `Rewind`, `Seek`, `Remove`', inline=False)
        embed.add_field(name="Filters", value='`Vaporwave`, `Lofi`, `8d`, `Slowmo`, `BassBoost`, `China`, `Chipmunk`, `DarthVader`, `Demon`, `Funny`, `Karoke`, `NightCore`, `Pop`, `Soft`, `TrebleBass`, `Tremolo`, `Alien`, `Reset`', inline=False)
        embed.add_field(name="Utility", value='`Avatar`, `Banner`, `MemberCount`, `Afk`', inline=False)
        embed.add_field(name="Info", value='`Ping`, `Purge`, `Uptime`, `Invite`, `Support`, `Stats`, `Setpreifx`, `Help`', inline=False)
        
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
        
        if query:
            command = self.client.get_command(query)
            if command:
                aliases = ", ".join(command.aliases)
                bablu=discord.Embed(color=Fluffy.color, description=f"**{command.help}**")
                bablu.add_field(name="Aliases", value=f"`{aliases}`", inline=False)
                bablu.add_field(name="Usage", value=f"`{command.usage}`", inline=False)
                bablu.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
                bablu.set_thumbnail(url=ctx.author.display_avatar.url)
                bablu.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=bablu)
                return
            else:
                await ctx.send("Command not found.")
                return

        message = await ctx.reply(embed=embed, view=view, mention_author=False)
        try:
            await asyncio.sleep(view.timeout)
        except asyncio.CancelledError:
            pass
        else:
            for child in view.children:
                child.disabled = True
            await message.edit(embed=embed, view=view)


async def setup(client):
    await client.add_cog(Help(client))