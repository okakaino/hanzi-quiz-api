import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class ItemDB(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    hanzi: Mapped[str]
    pinyin: Mapped[str]
    english: Mapped[str]
    img_url: Mapped[str]

def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()