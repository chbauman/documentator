from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Item)
        .filter(models.Item.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    item_dict = item.dict()
    db_item = models.Item(**item_dict, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def set_file_to_user_item(db: Session, upload_file_path: str, item_id: int):
    user_item = db.get(models.Item, item_id)
    if not user_item:
        raise HTTPException(status_code=404, detail="Hero not found")
    user_item.file_path = upload_file_path

    db.add(user_item)
    db.commit()
    db.refresh(user_item)
    return user_item


def find_user_item_file_path(db: Session, user_id: int, item_id: int):
    item = (
        db.query(models.Item)
        .filter(models.Item.owner_id == user_id)
        .filter(models.Item.id == item_id)
        .first()
    )
    return item.file_path
