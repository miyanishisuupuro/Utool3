import discord
from discord import app_commands
from discord.ext import commands

class CmdRm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cmd_role_id = 1356850745634324651
        self.admin_role_id = 1356850745634324651

    @app_commands.command(name="cmdrm", description="コマンド禁止コマンド")
    @app_commands.describe(user="コマンドを禁止にするユーザー")
    async def cmdrm(self, interaction: discord.Interaction, user: discord.Member):
        if not any(role.id == self.admin_role_id for role in interaction.user.roles):
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        cmd_role = interaction.guild.get_role(self.cmd_role_id)
        if cmd_role is None:
            await interaction.response.send_message("コマンド権限ロールが見つかりませんでした。", ephemeral=True)
            return

        try:
            await user.remove_roles(cmd_role)
            await interaction.response.send_message(f"{user.display_name} をコマンド禁止にしました。")
        except Exception as e:
            await interaction.response.send_message(f"ロール剥奪に失敗しました: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdRm(bot))
