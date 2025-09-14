from discord import app_commands, Interaction, Embed
from discord.ext import commands
from models.notification import Session, Notification

class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notify_group = app_commands.Group(name="notify", description="通知に関するコマンド")

        # サブコマンドの登録
        self.notify_group.command(name="configure", description="通知設定")(self.configure)
        self.notify_group.command(name="delete", description="通知設定削除")(self.delete)
        self.notify_group.command(name="status", description="通知設定確認")(self.status)

    async def configure(self, interaction: Interaction):
        voice = interaction.user.voice
        if not voice or not voice.channel:
            await interaction.response.send_message("ボイスチャンネルに入ってから実行してね。", ephemeral=True)
            return

        session = Session()
        notif = Notification(
            guild_id=str(interaction.guild_id),
            voice_channel_id=str(voice.channel.id),
            text_channel_id=str(interaction.channel_id)
        )
        session.merge(notif)
        session.commit()
        session.close()

        await interaction.response.send_message(f"{voice.channel.name} への入室通知をこのチャンネルに設定したよ～")

    async def delete(self, interaction: Interaction):
        session = Session()
        session.query(Notification).filter_by(
            guild_id=str(interaction.guild_id),
            text_channel_id=str(interaction.channel_id)
        ).delete()
        session.commit()
        session.close()
        await interaction.response.send_message("通知設定を削除したよ～")

    async def status(self, interaction: Interaction):
        session = Session()
        notifs = session.query(Notification).filter_by(
            guild_id=str(interaction.guild_id),
            text_channel_id=str(interaction.channel_id)
        ).all()
        session.close()

        if not notifs:
            await interaction.response.send_message("通知設定はありません。")
            return

        channels = "\n".join([f"<#{n.voice_channel_id}>" for n in notifs])
        embed = Embed(title="通知設定中のボイスチャンネル", description=channels)
        await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        existing = self.bot.tree.get_command("notify")
        if existing:
            self.bot.tree.remove_command("notify")
        self.bot.tree.add_command(self.notify_group)

async def setup(bot):
    await bot.add_cog(Notify(bot))
