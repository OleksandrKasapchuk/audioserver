from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    songs = relationship("Song",back_populates="parent")


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True,index=True)
    
    title = Column(String)
    description = Column(String)
    year = Column(Integer)

    path = Column(String)

    author_id = Column(Integer, ForeignKey("author.id"))
    
    parent = relationship("Author", back_populates="songs")