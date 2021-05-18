import discord
from discord.embeds import Embed
from discord.ext import commands
from logging import getLogger
import time
from discord.ext.commands.core import is_owner
from discord.ext.commands import Bot
from discord.colour import Colour

log = getLogger('extensions.moderation')

class ModCog(commands.Cog, name="Moderation"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(
        aliases=['clear'],
        description='Clears the chat'
    )
    async def cc(self, ctx, *, amount: int = None):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if amount is None:
                    await ctx.send("You must input a number")
                else:
                    deleted = await ctx.message.channel.purge(limit=amount)
                    await ctx.send(
                        f"Messages deleted by {ctx.message.author.mention}: `{len(deleted)}`"
                    )
                    time.sleep(1.5)
                    await ctx.message.channel.purge(limit=1)
            except:
                await ctx.send("I can not delete messages here.")
        else:
            await ctx.send("You do not have permissions to execute this command.")

    @commands.command(
        aliases=['k'],
        description='kicks a user from the guild'
    )
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason):
        if user.guild_permissions.manage_messages:
            await ctx.send("I can not kick this user because he is an admin/moderator.")
        elif ctx.message.author.guild_permissions.kick_members:
            if reason is None:
                await ctx.guild.kick(user=user, reason="None")
                await ctx.send(f"{user} has been kicked.")
            else:
                await ctx.guild.kick(user=user, reason=reason)
                await ctx.send(f"{user} has been kicked for {reason}.")
        else:
            await ctx.send("You do not have permissions do execute this command.")

    @commands.command(
        aliases=['b'],
        description='bans a user from the guild'
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        if user.guild_permissions.manage_messages:
            await ctx.send("I can not ban this user because he is an admin/moderator.")
        elif ctx.message.author.guild_permissions.ban_members:
            if reason is None:
                await ctx.guild.ban(user=user, reason="None")
                await ctx.send(f"{user} has been banned.")
            else:
                await ctx.guild.ban(user=user, reason=reason)
                await ctx.send(f"{user} has been banned.")
        else:
            await ctx.send("You do not have permissions do execute this command.")

    @commands.command(
        aliases=['ub'],
        description='unbans a user from the guild'
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} got unbanned")
                return

    @commands.command(
        aliases=["r"],
        description="restart the bot"
        )
    @is_owner()
    async def restart(self, ctx):
        embed = Embed(
            title= 'Restarting...',
            colour=Colour.dark_red(),
        )
        embed.set_author(
            name="SERVER"
        )
        embed.set_footer(
            text=self.bot.signature
        )
        await ctx.send(embed=embed)
        exit(104)

def setup(bot: Bot):
    bot.add_cog(ModCog(bot))
