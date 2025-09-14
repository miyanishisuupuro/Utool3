from sqlalchemy import Column, Integer, String
from models.youtube_db import Base  # 共通のBaseを使う

class YouTubeNotification(Base):
    __tablename__ = "youtube_notifications"

    id = Column(Integer, primary_key=True)
    guild_id = Column(String)
    youtube_channel_id = Column(String)
    text_channel_id = Column(String)
    last_video_id = Column(String, nullable=True)
