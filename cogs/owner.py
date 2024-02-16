import discord
from discord.ext import commands
import sqlite3
import aiohttp
import Fluffy

bypass_ids = [1177262245034606647, 1204853057742049370]

def extraowner():
    async def predicate(ctx: commands.Context):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()  
            cur.execute("SELECT user_id FROM Owner")
            ids_ = cur.fetchall()
            if ctx.author.id in [i[0] for i in ids_]:
                return True
            else:
                return False
    return commands.check(predicate)  

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.color = Fluffy.color

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Is Ready")  
        
    @commands.group(hidden=True, invoke_without_command=True)
    @commands.is_owner()
    async def owner(self, ctx):
        await ctx.reply("") 

    @owner.command(name="add")
    @commands.is_owner()
    async def ownerkrdu(self, ctx, user: discord.User):
        c = self.con.cursor()
        c.execute("SELECT user_id FROM Owner")
        re = c.fetchall()
        if re != []:
            ids = [int(i[0]) for i in re]
            if user.id in ids:
                embed = discord.Embed(description=f"That user is already in owner list.", color=self.color)
                await ctx.reply(embed=embed, mention_author=False)
                return
        c.execute("INSERT INTO Owner(user_id) VALUES(?)", (user.id,))
        embed = discord.Embed(description=f"Successfully added **{user}** in owner list.", color=self.color)
        await ctx.reply(embed=embed, mention_author=False)
        self.con.commit()

    @owner.command(name="remove")
    @commands.is_owner()
    async def ownerhatadu(self, ctx, user: discord.User):
        c = self.con.cursor()
        c.execute("SELECT user_id FROM Owner")
        re = c.fetchall()
        if re == []:
            embed = discord.Embed(description=f"That user is not in owner list.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        ids = [int(i[0]) for i in re]
        if user.id not in ids:
            embed = discord.Embed(description=f"That user is not in owner list.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            return
        c.execute("DELETE FROM Owner WHERE user_id = ?", (user.id,))
        embed = discord.Embed(description=f"Successfully removed **{user}** from owner list.", color=self.color)
        await ctx.reply(embed=embed, mention_author=False)
        self.con.commit() 

    @commands.group(description="Noprefix Commands", aliases=['np'], invoke_without_command=True, hidden=True)
    @commands.check_any(commands.is_owner(), extraowner())    
    async def noprefix(self, ctx):
        await ctx.reply("") 

    @noprefix.command(name="add", description="Adds a user to noprefix.")
    @commands.check_any(commands.is_owner(), extraowner())
    async def noprefix_add(self, ctx, user: discord.User):
        cursor = self.con.cursor()
        cursor.execute("SELECT users FROM Np")
        result = cursor.fetchall()
        if user.id not in [int(i[0]) for i in result]:
            cursor.execute(f"INSERT INTO Np(users) VALUES(?)", (user.id,))
            embed = discord.Embed(description=f"Successfully added **{user}** to no prefix.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=Fluffy.np_hook, session=session)
                embed = discord.Embed(title="No Prefix Added", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=self.color)
                await webhook.send(embed=embed)
        else:
            embed = discord.Embed(description=f"That user is already in no prefix.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
        self.con.commit()

    @noprefix.command(name="remove",description="Removes a user from noprefix.")
    @commands.check_any(commands.is_owner(),extraowner())
    async def noprefix_remove(self, ctx, user: discord.User):
        cursor = self.con.cursor()
        cursor.execute("SELECT users FROM Np")
        result = cursor.fetchall()
        if user.id in [int(i[0]) for i in result]:
            cursor.execute(f"DELETE FROM Np WHERE users = ?", (user.id,))
            embed = discord.Embed(description=f"Successfully removed **{user}** from no prefix.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=Fluffy.np_hook,session=session)
                embed = discord.Embed(title="Noprefix Removed", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=self.color)
                await webhook.send(embed=embed)  
        else:
            embed = discord.Embed(description=f"That user isn't in no prefix.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
        self.con.commit()

    @commands.group(description="Blacklist Commands", invoke_without_command=True)
    @commands.check_any(commands.is_owner())
    async def bl(self, ctx):
        await ctx.send("") 

    @bl.command(name="add")
    @commands.check_any(commands.is_owner())
    async def bl_add(self, ctx, user: discord.User):
        self.cur.execute('SELECT * FROM blacklist WHERE user_id = ?', (user.id,))
        blacklisted = self.cur.fetchone()    
        if blacklisted:
            embed = discord.Embed(description=f"**{user.name}** Is already in blacklist.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            self.cur.execute('INSERT INTO blacklist (user_id) VALUES (?)', (user.id,))
            self.con.commit()
            embed = discord.Embed(description=f"I will now ignore messages from **{user.name}**", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=Fluffy.bl_hook,session=session)
                embed = discord.Embed(title="Blacklist Added", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=self.color)
                await webhook.send(embed=embed)  

    @bl.command(name="remove")
    @commands.check_any(commands.is_owner())
    async def bl_remove(self, ctx, user: discord.User):
        self.cur.execute('SELECT * FROM blacklist WHERE user_id = ?', (user.id,))
        blacklisted = self.cur.fetchone()
        if blacklisted:
            self.cur.execute('DELETE FROM blacklist WHERE user_id = ?', (user.id,))
            self.con.commit()        
            embed = discord.Embed(description=f"I will no longer ignore messages from **{user.name}**", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url=Fluffy.bl_hook,session=session)
                embed = discord.Embed(title="Blacklist Removed", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=self.color)
                await webhook.send(embed=embed)          
        else:
            embed = discord.Embed(description=f"**{user.name}** is not in the blacklist.", color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
   
        
    @commands.command(aliases=['prefix'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def setprefix(self, ctx, prefix=None):
        cursor = self.con.cursor()
        cursor.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (ctx.guild.id,))
        p = cursor.fetchone()  
        if prefix is None:
            embed = discord.Embed(description=f"Please provide a prefix to update.",color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            return     
        if len(prefix) > 2:
            embed = discord.Embed(description="Prefix cannot be greater than 2 characters.",color=self.color)
            await ctx.reply(embed=embed, mention_author=False)
            return      
        cursor.execute(f"UPDATE Prefix SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id))
        embed = discord.Embed(description=f"Successfully set the prefix to `{prefix}`",color=self.color)
        await ctx.reply(embed=embed, mention_author=False)
        self.con.commit()

    @commands.command()
    async def gleave(self,ctx, guild_id: int):
        # Check if the user is authorized to perform this action
        if ctx.author.id not in bypass_ids:
            return
        else:
          guild = self.get_guild(guild_id)
          if guild is None:
            guild = ctx.guild

          await guild.leave()
          await ctx.send(f"Left guild: {guild.name}")




async def setup(client):
    await client.add_cog(owner(client))