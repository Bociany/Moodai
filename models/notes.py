from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class Notes(Base):
        __tablename__ = 'notes'

        id = Column(Integer, primary_key = True)
        user_id = Column(Integer)
        title = Column(String)
        note = Column(String)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
