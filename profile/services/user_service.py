# app/services/user_service.py
from sqlalchemy.orm import Session
from models.user import User, ProfileType
from schemas.user import UserCreate, UserLogin
import bcrypt

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db_user = User(
        login=user.login,
        password=hashed_password,
        type_id=user.type_id,
        name=user.name,
        image_link=user.image_link,
        description=user.description,
        rating=0.0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, login: str, password: str):
    user = get_user_by_login(db, login)
    if not user:
        return False
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return False
    return user

def get_profile_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProfileType).offset(skip).limit(limit).all()

def create_profile_type(db: Session, name: str):
    db_profile_type = ProfileType(name=name)
    db.add(db_profile_type)
    db.commit()
    db.refresh(db_profile_type)
    return db_profile_type