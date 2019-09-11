from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from getpolicy import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "scraped"

    id = Column(Integer, primary_key=True)
    privacy = Column('privacy', Text)
    terms = Column('terms', Text)
    rest_url = Column('rest_url', Text)
    url = Column('url', Text)
    fail = Column('fail', Text)
    domain = Column('domain', Text)