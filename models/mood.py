from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class Mood(Base):
        __tablename__ = 'mood'

        id = Column(Integer, primary_key = True)
        user_id = Column(Integer)
        mood = Column(Integer)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
