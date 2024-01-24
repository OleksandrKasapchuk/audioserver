from sqlalchemy.orm import Session
from . import models, schemas

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_author_songs(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    if not author_id:
        songs = db.query(models.Song).offset(skip).limit(limit).all()
    else:
        songs = db.query(models.Song).filter(models.Song.author_id == author_id).all()

    return songs

def update_author(db: Session, author: schemas.Author):
    db_author = db.query(models.Author).filter(models.Author.id == author.id).first()
    if db_author:
        db_author.name = author.name
        db.commit()
        db.refresh(db_author)
       
def delete_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    
def get_all_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).offset(skip).limit(limit).all()

def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def create_author_song(db: Session, song: schemas.SongCreate, author_id: int):
    db_song = models.Song(**song.model_dump(), parent_id=author_id)

    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    return db_song
