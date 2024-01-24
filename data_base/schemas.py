from typing import Union
from pydantic import BaseModel
# from settings import AUDIOS_PATH
# import os

class SongBase(BaseModel):
    title: str
    description: Union[str, None] = None

    year: int



class SongCreate(SongBase):
    pass


class Song(SongBase):
    id: int
    author_id: int
    
    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    songs: list[Song] = []

    class Config:
        from_attributes = True