import discord
from discord import app_commands
from discord.ext import commands
from main import nerfed_users  # グローバルセットを参照

class Nerf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nerf_role_id = 1303270351429697586
        self.admin_role_id = 1356850745634324651

    @app_commands.command(name="nerf", description="全ステータス大ダウンコマンド")
    @app_commands.describe(user="全ステータス大ダウンにするユーザー")
    async def nerf(self, interaction: discord.Interaction, user: discord.Member):
        if not any(role.id == self.admin_role_id for role in interaction.user.roles):
            await interaction.response.send_message("権限がないみたい…", ephemeral=True)
            return

        nerf_role = interaction.guild.get_role(self.nerf_role_id)
        if nerf_role is None:
            await interaction.response.send_message("ロールが見つかりませんでした。", ephemeral=True)
            return

        try:
            await user.add_roles(nerf_role)
            nerfed_users.add(user.id)  # グローバルセットに追加
            await interaction.response.send_message(f"{user.display_name} を全ステータス大ダウンしました。")
        except Exception as e:
            await interaction.response.send_message(f"ロール付与に失敗しました: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Nerf(bot))
