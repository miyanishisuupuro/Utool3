from discord import app_commands, Interaction, Embed
from discord.ext import commands
from models.youtube_db import Session, YouTubeChannel


class YouTubeNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_group = app_commands.Group(name="youtube", description="YouTube通知の設定")

        # サブコマンドの登録
        self.youtube_group.command(name="add", description="通知するYouTubeチャンネルを追加")(self.add)
        self.youtube_group.command(name="remove", description="通知チャンネルを削除")(self.remove)
        self.youtube_group.command(name="list", description="通知対象のチャンネル一覧を表示")(self.list_channels)

    async def add(self, interaction: Interaction, channel_id: str):
        session = Session()
        existing = session.query(YouTubeChannel).filter_by(
            guild_id=str(interaction.guild_id),
            channel_id=channel_id
        ).first()

        if existing:
            await interaction.response.send_message("そのチャンネルはすでに登録されています。", ephemeral=True)
        else:
            yt = YouTubeChannel(
                guild_id=str(interaction.guild_id),
                text_channel_id=str(interaction.channel_id),
                channel_id=channel_id
            )
            session.add(yt)
            session.commit()
            await interaction.response.send_message(f"チャンネルID `{channel_id}` を通知対象に追加しました！")

        session.close()

    async def remove(self, interaction: Interaction, channel_id: str):
        session = Session()
        deleted = session.query(YouTubeChannel).filter_by(
            guild_id=str(interaction.guild_id),
            text_channel_id=str(interaction.channel_id),
            channel_id=channel_id
        ).delete()
        session.commit()
        session.close()

        if deleted:
            await interaction.response.send_message("チャンネルを削除しました。")
        else:
            await interaction.response.send_message("そのチャンネルは登録されていません。", ephemeral=True)

    async def list_channels(self, interaction: Interaction):
        session = Session()
        channels = session.query(YouTubeChannel).filter_by(
            guild_id=str(interaction.guild_id),
            text_channel_id=str(interaction.channel_id)
        ).all()
        session.close()

        if not channels:
            await interaction.response.send_message("登録されているチャンネルはありません。", ephemeral=True)
            return

        description = "\n".join([f"`{ch.channel_id}`" for ch in channels])
        embed = Embed(title="通知対象のYouTubeチャンネル一覧", description=description)
        await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        existing = self.bot.tree.get_command("youtube")
        if existing:
            self.bot.tree.remove_command("youtube")
        self.bot.tree.add_command(self.youtube_group)

async def setup(bot):
    await bot.add_cog(YouTubeNotify(bot))
