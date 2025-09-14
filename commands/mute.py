import discord
from discord import app_commands
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_role_id = 1288263740680306750
        self.admin_role_id = 1356850745634324651

    @app_commands.command(name="mute", description="ミュートコマンド")
    @app_commands.describe(user="ミュートにするユーザー")
    async def mute(self, interaction: discord.Interaction, user: discord.Member):
        if not any(role.id == self.admin_role_id for role in interaction.user.roles):
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        mute_role = interaction.guild.get_role(self.mute_role_id)
        if mute_role is None:
            await interaction.response.send_message("ミュートロールが見つかりませんでした。", ephemeral=True)
            return

        try:
            await user.add_roles(mute_role)
            await interaction.response.send_message(f"{user.display_name} をミュートしました。")
        except Exception as e:
            await interaction.response.send_message(f"ロール付与に失敗しました: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mute(bot))
