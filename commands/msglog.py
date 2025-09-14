import discord
from discord import app_commands
from discord.ext import commands
from models.youtube_db import Session
from models.message_log import MessageLog

class MsgLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="msglog",
        description="過去のメッセージ履歴を検索します"
    )
    @app_commands.describe(
        user="ユーザーを指定（省略可）",
        channel="チャンネルを指定（省略可）",
        limit="直近何件を表示するか（最大50件）"
    )
    async def msglog(self, interaction: discord.Interaction, user: discord.User = None,
                     channel: discord.TextChannel = None, limit: int = 10):
        limit = min(limit, 50)  # 上限50件
        session = Session()

        query = session.query(MessageLog)
        if user:
            query = query.filter(MessageLog.author_id == str(user.id))
        if channel:
            query = query.filter(MessageLog.channel_id == str(channel.id))

        query = query.order_by(MessageLog.created_at.desc()).limit(limit)
        logs = query.all()
        session.close()

        if not logs:
            await interaction.response.send_message("🔍 該当するメッセージがありません。", ephemeral=True)
            return

        embed = discord.Embed(
            title="📜 メッセージ履歴",
            color=discord.Color.blue()
        )

        for log in logs[::-1]:  # 古い順に表示
            author = self.bot.get_user(int(log.author_id))
            chan = self.bot.get_channel(int(log.channel_id))
            content = log.content
            ts = log.created_at.strftime("%Y-%m-%d %H:%M")
            if log.edited_at:
                content += f" *(編集済み {log.edited_at.strftime('%H:%M')})*"
            embed.add_field(
                name=f"{author.display_name if author else '不明'} - #{chan.name if chan else '不明'} ({ts})",
                value=content,
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(MsgLog(bot))
