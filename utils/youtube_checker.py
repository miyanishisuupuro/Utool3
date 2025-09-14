from discord.ext import tasks
from models.youtube_db import Session, YouTubeChannel
from models.youtube import get_latest_video
import discord

def start_youtube_check(bot: discord.Client):
    @tasks.loop(minutes=5)
    async def check_youtube():
        session = Session()
        all_channels = session.query(YouTubeChannel).all()

        for ch in all_channels:
            latest = get_latest_video(ch.channel_id)
            if not latest:
                continue

            if latest["id"] != ch.last_video_id:
                ch.last_video_id = latest["id"]
                session.commit()

                text_channel = bot.get_channel(int(ch.text_channel_id))
                if text_channel:
                    await text_channel.send(
                        f"📢 **新しい動画が投稿されました！**\n"
                        f"**{latest['title']}**\n{latest['url']}"
                    )

        session.close()

    check_youtube.start()

__all__ = ['start_youtube_check']
