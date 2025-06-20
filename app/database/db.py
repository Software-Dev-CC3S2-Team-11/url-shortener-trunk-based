from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


URL = getenv('URL')

engine = create_engine(URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Crea una sesión de base de datos y la devuelve.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
