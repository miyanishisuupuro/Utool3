# models/message_log.py
from sqlalchemy import Column, String, DateTime, Text
from models.youtube_db import Base
import datetime

class MessageLog(Base):
    __tablename__ = "message_logs"

    message_id = Column(String, primary_key=True)   # DiscordメッセージID
    channel_id = Column(String, nullable=False)
    author_id = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    edited_at = Column(DateTime, nullable=True)
