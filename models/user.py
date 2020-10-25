from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key = True)
	email = Column(String)
	fullname = Column(String)
	password = Column(String)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
