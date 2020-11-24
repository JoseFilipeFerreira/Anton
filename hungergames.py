import discord
from discord.ext import commands
import json
import math

class HungerGames(commands.Cog):
    def __init__(self, bot):
        self.bot =bot
        stats = json.load(open(self.bot.STATS_PATH, 'r'))

        self.member_stats = stats["members"]
        self.message_channel = stats["message_channel"]


    @commands.command(name='images',
        description="list all available Images",
        brief="all available Images")
    async def images(self, ctx):
        embed=discord.Embed(
            title="Image",
            description="all photos",
            color=self.bot.embed_color
        )
        array = []
        for pic in self.bot.mediaMap:
            array.append(pic)
        array.sort()

        embed.add_field(name="📸", value='\n'.join(array), inline=True)
        await ctx.message.author.send(embed=embed)

    @commands.command(name='point',
                      description="give one point to a mentioned user",
                      brief="give point")
    @commands.has_permissions(administrator=True)
    async def point(self, ctx, member : discord.Member, points:int = 1):
        if str(member.id) in self.member_stats:
            self.member_stats[str(member.id)] += points
        else:
            self.member_stats[str(member.id)] = points

        self.save_stats()
        await self.send_leaderboard(ctx)

    @commands.command(name='channel',
                      description="change leaderboard channel",
                      brief="change leaderboard channel")
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx):
        self.message_channel = ctx.message.channel.id
        await ctx.send("This is the new leaderboard channel")
        self.save_stats()
        await self.send_leaderboard(ctx)

    async def send_leaderboard(self, ctx):
        message = "🏆 **RANK** 🏆\n"

        for id in sorted(self.member_stats, key=self.member_stats.__getitem__, reverse=True):
            member = self.bot.get_user(int(id))
            if member:
                message += member.mention
                message += ": "
                message += str(self.member_stats[id])
                message += "\n"
            else:
                print("User", id, "not in the guild")

        message += "\n\n"
        message += "**Por Cultos:**\n"

        
        cults = {}
        active_members = {}
        for role in ctx.message.guild.roles:
            if "culto" in role.name.lower():
                cults[role.id] = 0
                active_members[role.id] = 0
                for member in role.members:
                    cults[role.id] += self.member_stats.get(str(member.id), 0)
                    active_members[role.id] += 1 if str(member.id) in self.member_stats else 0

        cult_list = list(cults.keys())
        cult_list.sort(key=lambda id:cults[id]/active_members[id] if active_members[id] else 0, reverse=True)

        for id in cults:
            role = ctx.message.guild.get_role(int(id))
            if role:
                message += role.mention
                message += ": "
                message += str(cults[id])
                message += " ("
                message += str(math.ceil(cults[id]/active_members[id] if active_members[id] else 0))
                message += ")\n"
            else:
                print("Role", id, "not in the guild")

        channel = ctx.bot.get_channel(self.message_channel)

        mgs = []
        async for x in channel.history(limit=10):
            mgs.append(x)

        await channel.delete_messages(mgs)

        msg = await channel.send("Loading...")

        await msg.edit(content=message)
            

    def save_stats(self):
        stats = {}
        stats["members"] = self.member_stats
        stats["message_channel"] = self.message_channel

        with open(self.bot.STATS_PATH, 'w') as file:
            json.dump(stats, file, indent=4)


def setup(bot):
    bot.add_cog(HungerGames(bot)) 
