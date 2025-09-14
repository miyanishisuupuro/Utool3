import discord
from discord import app_commands
from discord.ext import commands

class CmdAd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd_role_id = 1356850745634324651
        self.admin_role_id = 1356850745634324651

    @app_commands.command(name="cmdad", description="コマンド許可")
    @app_commands.describe(user="コマンドを許可するユーザー")
    async def cmdad(self, interaction: discord.Interaction, user: discord.Member):
        # 管理者権限チェック
        if not any(role.id == self.admin_role_id for role in interaction.user.roles):
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        cmd_role = interaction.guild.get_role(self.cmd_role_id)
        if cmd_role is None:
            await interaction.response.send_message("コマンド権限ロールが見つかりませんでした。", ephemeral=True)
            return

        try:
            await user.add_roles(cmd_role)
            await interaction.response.send_message(f"{user.display_name} にコマンドを許可しました。")
        except Exception as e:
            await interaction.response.send_message(f"ロール付与に失敗しました: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdAd(bot))
