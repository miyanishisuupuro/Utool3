import discord
from discord.ext import commands
import json
import os

CONFIG_FILE = "channel_config.json"

class SetChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setchannel")
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """通知用のチャンネルを設定します"""
        # 設定を読み込み
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        else:
            config = {}

        # ギルドIDをキーにチャンネルIDを保存
        config[str(ctx.guild.id)] = channel.id

        # 設定を保存
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

        await ctx.send(f"✅ 通知チャンネルを {channel.mention} に設定しました！")

async def setup(bot):
    await bot.add_cog(SetChannel(bot))
