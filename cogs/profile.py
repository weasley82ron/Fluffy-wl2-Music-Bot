import discord
from discord.ext import commands
import Fluffy
import json
from premoji import emojis


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

    async def load_badges(self):
        try:
            with open('badges.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    async def save_badges(self, badges):
        with open('badges.json', 'w') as f:
            json.dump(badges, f, indent=4)

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
            embed = discord.Embed(title="Error", color=Fluffy.color, description="Please provide a badge number.")
            
            embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
            embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
            await ctx.send(embed=embed)
            return
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            badges = await self.load_badges()
            badge_name = get_badge_name(badge_number)
            if badge_name == "Unknown":
                embed = discord.Embed(title="Error", color=Fluffy.color, description="Not a valid badge! Use `badge list` command.")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)
                return
            
            user_id = str(user.id)
            user_badges = badges.get(user_id, [])
            if badge_number not in user_badges:
                user_badges.append(badge_number)
                badges[user_id] = user_badges
                await self.save_badges(badges)
                embed = discord.Embed(title="Badge Given", color=Fluffy.color, description=f"Badge `{badge_name}` given to {user.display_name}")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", color=Fluffy.color, description=f"{user.display_name} already has badge `{badge_name}`")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)

    @badge.command()
    async def remove(self, ctx, badge_number: int=None, user: discord.User=None):
        if not badge_number:
            embed = discord.Embed(title="Error", color=Fluffy.color, description="Please provide a badge number.")
            
            embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
            embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
            await ctx.send(embed=embed)
            return
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            badges = await self.load_badges()
            badge_name = get_badge_name(badge_number)
            if badge_name == "Unknown":
                embed = discord.Embed(title="Error", color=Fluffy.color, description="Not a valid badge! Use `badge list` command.")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)
                return
            
            user_id = str(user.id)
            user_badges = badges.get(user_id, [])
            if badge_number in user_badges:
                user_badges.remove(badge_number)
                badges[user_id] = user_badges
                await self.save_badges(badges)
                embed = discord.Embed(title="Badge Removed", color=Fluffy.color, description=f"Badge `{badge_name}` removed from {user.display_name}")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", color=Fluffy.color, description=f"{user.display_name} doesn't have badge `{badge_name}`")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)

    @badge.command()
    async def giveall(self, ctx, user: discord.User=None):
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            badges = await self.load_badges()
            user_id = str(user.id)
            badges[user_id] = list(BADGE_NAMES.keys())
            await self.save_badges(badges)
            embed = discord.Embed(title="All Badges Given", color=Fluffy.color, description=f"All badges given to {user.display_name}")
            
            embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
            embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
            await ctx.send(embed=embed)

    @badge.command()
    async def removeall(self, ctx, user: discord.User=None):
        if not user:
            user = ctx.author
        if ctx.author.id in badge_givers:
            badges = await self.load_badges()
            user_id = str(user.id)
            if user_id in badges:
                del badges[user_id]
                await self.save_badges(badges)
                embed = discord.Embed(title="All Badges Removed", color=Fluffy.color, description=f"All badges removed from {user.display_name}")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Error", color=Fluffy.color, description=f"{user.display_name} doesn't have any badges")
                
                embed.set_thumbnail(url=user.display_avatar.url or ctx.author.display_avatar.url)
                embed.set_footer(text="By Fluffy Services", icon_url=Fluffy.icon)
                await ctx.send(embed=embed)

    @commands.command(aliases=["pr"])
    async def profile(self, ctx, user: discord.User=None):
        if not user:
            user = ctx.author
        badges = await self.load_badges()
        user_id = str(user.id)
        user_badges = badges.get(user_id, [])
        
        if user_badges:
            badge_names = [get_badge_name(badge_number) for badge_number in user_badges]
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