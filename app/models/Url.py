from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, Integer
from database.db import Base


class URL(Base):
    __tablename__ = "Url"

    original = Column(Text)
    shorter = Column(Text, primary_key=True)
    username = Column(Text, ForeignKey("users.username"))
    visits = Column(Integer)
    created_at = Column(TIMESTAMP)
    expire_at = Column(TIMESTAMP)