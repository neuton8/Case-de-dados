from sqlalchemy import Integer, String, ForeignKey, Column, Float,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signal'

    signal_id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    mean = Column(Float)
    min = Column(Float)
    max = Column(Float)
    std = Column(Float)
    timestamp = Column(DateTime)

    def __init__(self, name, media, min, max, std, timestamp):
        self.name = name
        self.media = media
        self.min = min
        self.max = max
        self.std = std
        self.timestamp = timestamp


def create_tables(DATABASE_URL):
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker( bind=engine)
    SessionLocal = SessionLocal()
    Base.metadata.create_all(engine)
