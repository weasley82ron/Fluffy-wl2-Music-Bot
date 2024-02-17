import discord
from discord.ext import commands
import Fluffy
from premoji import emojis
import sqlite3

badge_givers = [1204853057742049370, 1177262245034606647, 1193351155426787451]

def get_badge_name(badge_number):
    badges = {
        1: "Developer",
        2: "Owner",
        3: "Admin",
        4: "Mod",
        5: "Support Team",
        6: "Bug Hunter",
        7: "Supporter",
        8: "Friends"
    }
    return badges.get(badge_number, "Unknown")

BADGE_NAMES = {
        1: "Developer",
        2: "Owner",
        3: "Admin",
        4: "Mod",
        5: "Support Team",
        6: "Bug Hunter",
        7: "Supporter",
        8: "Friends"
    }

class profile(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = Fluffy.color
        self.connection = sqlite3.connect("badges.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS badges (
                               user_id INTEGER,
                               badge_number INTEGER
                               )""")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile Is Ready")

    @commands.group(invoke_without_command=True)
    async def badge(self, ctx):
        embed = discord.Embed(title="Badges", color=Fluffy.color, description="""
**give** - Gives The Badge To The User.
**remove** - Removes The Badge From The User.
**giveall** - Gives All Badges To The User.
**removeall** - Remove All Badges From The User.
**profile** - Shows Your Badges.
**list** - Shows Badge List.
        """)
        await ctx.send(embed=embed)

    @badge.command()
    async def list(self, ctx):
        embed = discord.Embed(title="Badge List", color=Fluffy.color, description="""
1 . Developer
2 . Owner
3 . Admin
4 . Mod
5 . Support Team
6 . Bug Hunter
7 . Supporter
8 . Friends
""")
        
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
        await ctx.send(embed=embed)

    @badge.command()
    async def give(self, ctx, badge_number: int=None, user: discord.User=None):
        if not badge_number:
            # Error handling
            return
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            # Add badge to the database for the user
            self.cursor.execute("INSERT INTO badges (user_id, badge_number) VALUES (?, ?)", (user.id, badge_number))
            self.connection.commit()
            # Confirmation message
            await ctx.send(f"Badge {get_badge_name(badge_number)} given to {user.display_name}")

    @badge.command()
    async def remove(self, ctx, badge_number: int=None, user: discord.User=None):
        if not badge_number:
            # Error handling
            return
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            # Remove badge from the database for the user
            self.cursor.execute("DELETE FROM badges WHERE user_id = ? AND badge_number = ?", (user.id, badge_number))
            self.connection.commit()
            # Confirmation message
            await ctx.send(f"Badge {get_badge_name(badge_number)} removed from {user.display_name}")

    @badge.command()
    async def giveall(self, ctx, user: discord.User=None):
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            # Add all badges to the database for the user
            for badge_number in BADGE_NAMES.keys():
                self.cursor.execute("INSERT INTO badges (user_id, badge_number) VALUES (?, ?)", (user.id, badge_number))
            self.connection.commit()
            # Confirmation message
            await ctx.send(f"All badges given to {user.display_name}")

    @badge.command()
    async def removeall(self, ctx, user: discord.User=None):
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            # Remove all badges from the database for the user
            self.cursor.execute("DELETE FROM badges WHERE user_id = ?", (user.id,))
            self.connection.commit()
            # Confirmation message
            await ctx.send(f"All badges removed from {user.display_name}")

    @commands.command(aliases=["pr"])
    async def profile(self, ctx, user: discord.User=None):
        if not user:
            user = ctx.author
        self.cursor.execute("SELECT badge_number FROM badges WHERE user_id = ?", (user.id,))
        user_badges = self.cursor.fetchall()
        
        if user_badges:
            badge_names = [get_badge_name(badge[0]) for badge in user_badges]
            embed = discord.Embed(title=f"{user.display_name}'s Badges", color=Fluffy.color)
            description = ""
            for badge_name in badge_names:
                emoji_name = emojis.get(badge_name, ":white_check_mark:")  # Get emoji from premojis
                description += f"{emoji_name} {badge_name}\n"
            embed.description = description
        else:
            embed = discord.Embed(color=Fluffy.color)
            embed.add_field(name="Badges", value="`No Badges Available`")

        embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
        embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(profile(client))
