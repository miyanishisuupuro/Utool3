from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'
    guild_id = Column(String, primary_key=True)
    voice_channel_id = Column(String, primary_key=True)
    text_channel_id = Column(String)

engine = create_engine('sqlite:///db/notification.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
