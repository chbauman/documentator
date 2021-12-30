from typing import List
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, File
from fastapi.datastructures import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from db_app import crud, models, schemas
from db_app.database import SessionLocal, engine
from db_app.util import get_file_path

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/users/{user_id}/items/", response_model=List[schemas.Item])
def read_user_items(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    items = crud.get_user_items(db, user_id, skip=skip, limit=limit)
    return items


@app.post("/users/{user_id}/items/{item_id}/file/", response_model=schemas.Item)
async def add_file_to_item(
    item_id: int,
    user_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = get_file_path(user_id, image.filename)
    with open(file_path, "wb+") as f:
        f.write(image.file.read())
        f.close()

    return crud.set_file_to_user_item(db, str(file_path), item_id)


@app.get("/users/{user_id}/items/{item_id}/file/")
async def get_item_file(item_id: int, user_id: int, db: Session = Depends(get_db)):
    file_path = crud.find_user_item_file_path(db, user_id, item_id)
    return FileResponse(file_path)
