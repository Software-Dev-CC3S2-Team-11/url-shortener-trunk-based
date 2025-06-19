from database.db import Base
from sqlalchemy import Column, Text, Integer


class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text)
    email = Column(Text)
    password = Column(Text)
