from sqlalchemy import *
from .base import Base
from sqlalchemy import Column, Integer, Float

class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True) # Required for SQLAlchemy Mapping
    x = Column(Float)
    y = Column(Float)