from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class YouTubeChannel(Base):
    __tablename__ = "youtube_channels"

    guild_id = Column(String, primary_key=True)
    text_channel_id = Column(String, primary_key=True)
    channel_id = Column(String, primary_key=True)
    last_video_id = Column(String)  # 最後に通知した動画のID

engine = create_engine("sqlite:///youtube.db")  # SQLite の場合
Session = sessionmaker(bind=engine)
