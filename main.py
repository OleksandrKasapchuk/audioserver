from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


from sqlalchemy.orm import Session
from data_base import crud, models, schemas
from data_base.db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

# Залежність
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Статичні файли
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблони
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/authors", response_model=list[schemas.Author])
def read_authors(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return templates.TemplateResponse("authors.html", {"request": request, "authors": authors})

@app.get("/authors/add")
def get_form_add_author(request: Request):
    return templates.TemplateResponse("add_author.html", {"request": request})

@app.post("/authors/add", response_model=schemas.Author)
def add_author(request: Request, name: str = Form(),skip: int = 0, limit: int = 100, db: Session = Depends(get_db), ):
    errors = []
    authors = crud.get_authors(db, skip=skip, limit=limit)
    for author in authors:
        if name == author.name:
            errors.append('Author already exists')
    if len(errors) == 0:    
        crud.create_author(db=db, author=schemas.AuthorCreate(name=name)) 
        return RedirectResponse("/authors/", status_code=303)
    else:
        return templates.TemplateResponse("add_author.html", {"request": request, "errors": errors})


# Edit user FORM
@app.get("/author{author_id}/edit/")
def get_author(request: Request, author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(author_id=author_id, db=db)

    return templates.TemplateResponse("edit_author.html", {"request": request, "author": author})


@app.post("/author{author_id}/edit/")
def edit_author(author_id: int, db: Session = Depends(get_db), name: str = Form()):
    author = schemas.Author(id =author_id, name=name)
    crud.update_author(author=author, db=db)
    
    return RedirectResponse("/authors", status_code=303)

@app.get("/author{author_id}/delete/")
def delete_item(author_id: int, db: Session = Depends(get_db),):
    crud.delete_author(author_id=author_id, db=db)

    return RedirectResponse("/authors", status_code=303)


@app.get("/author{author_id}/song/add")
def create_song_for_author(request: Request):
    return templates.TemplateResponse("add_song.html", {"request": request})     


@app.post("/author{author_id}/song/add")
def create__song(title: str = Form(), description: str = Form(), year: int = Form(), author_id: int = None, db: Session = Depends(get_db), request: Request = None):
    crud.create_author_song(db=db, song=schemas.SongCreate(title=title, description=description, year=year, author_id=author_id)) 

    return RedirectResponse("/author{author_id}/songs/", status_code=303)


@app.get("/songs")
def read_songs(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_all_songs(db, skip=skip, limit=limit)
    return templates.TemplateResponse("all_songs.html", {"request": request, "songs": songs})


@app.get("/author{author_id}/songs/", response_model=list[schemas.Song])
def read_songs(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), author_id: int = None):
    songs = crud.get_author_songs(db, author_id, skip=skip, limit=limit)
    author = crud.get_author(db, author_id)
    return templates.TemplateResponse("author_songs.html", {"request": request, "songs": songs, "author": author})


@app.post("/author{author_id}/songs/", response_model=schemas.Song)
def create_song_for_author(author_id: int, song: schemas.SongCreate, db: Session = Depends(get_db)):
    return crud.create_author_song(db=db, song=song, author_id=author_id)