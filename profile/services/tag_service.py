# app/services/tag_service.py
from sqlalchemy.orm import Session
from models.tag import Tag, TagForUser
from schemas.tag import TagCreate, TagForUserCreate

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.tag_id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).filter(Tag.tag_type_id == 1).offset(skip).limit(limit).all()

def get_tags_by_type(db: Session, tag_type_id: int, skip: int = 0, limit: int = 100):
    return db.query(Tag).filter(Tag.tag_type_id == tag_type_id).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def assign_tag_to_user(db: Session, tag_for_user: TagForUserCreate):
    db_tag_for_user = TagForUser(**tag_for_user.dict())
    db.add(db_tag_for_user)
    db.commit()
    db.refresh(db_tag_for_user)
    return db_tag_for_user

def get_tags_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(TagForUser).filter(TagForUser.user_id == user_id).offset(skip).limit(limit).all()

def remove_tag_from_user(db: Session, tag_id: int, user_id: int):
    db_tag_for_user = db.query(TagForUser).filter(
        TagForUser.tag_id == tag_id,
        TagForUser.user_id == user_id
    ).first()
    if db_tag_for_user:
        db.delete(db_tag_for_user)
        db.commit()
    return db_tag_for_user