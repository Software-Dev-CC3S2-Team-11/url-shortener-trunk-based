from sqlalchemy import Column, Text, TIMESTAMP, Integer
from database.db import Base


class URL(Base):
    __tablename__ = 'Url'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    original = Column(Text)
    shorter = Column(Text, unique=True)
    username = Column(Text)
    visits = Column(Integer)
    created_at = Column(TIMESTAMP)
    expires_at = Column(TIMESTAMP)
