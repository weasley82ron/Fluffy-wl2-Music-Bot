import discord
import sqlite3
from discord.ext import commands

class nova(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.spam_count = {}

    @commands.Cog.listener()
    async def on_command(self, ctx):
        user_id = ctx.author.id
        self.cur.execute("SELECT 1 FROM blacklist WHERE user_id = ?", (user_id,))
        if self.cur.fetchone():
            return
        
        if user_id not in self.spam_count:
            self.spam_count[user_id] = 0

        self.spam_count[user_id] += 1

        if self.spam_count[user_id] > 5:
            self.cur.execute("INSERT OR IGNORE INTO blacklist (user_id) VALUES (?)", (user_id,))
            self.con.commit()
            await self.send_blacklist_dm(ctx.author)
        else:
            await ctx.invoke(ctx.command)
        
    async def send_blacklist_dm(self, user):
        embed = discord.Embed(
            description="You are blacklisted from using my commands due to spamming.",
            color=0xEB8DC0
        )
          await user.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        user_id = ctx.author.id
        if user_id in self.spam_count and self.spam_count[user_id] > 0:
            self.spam_count[user_id] = 0

async def setup(client):
    await client.add_cog(Nova(client))
