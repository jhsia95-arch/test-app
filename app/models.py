# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

from sqlalchemy import Column, Integer, String
# from database import Base
from app.database import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
