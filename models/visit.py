from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class Visit(Base):
        __tablename__ = 'visits'

        id = Column(Integer, primary_key = True)
        user_id = Column(Integer)
        scheduled_for = Column(DateTime, default=datetime.datetime.utcnow)
        note = Column(String)

