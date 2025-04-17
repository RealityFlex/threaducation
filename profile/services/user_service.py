# app/services/user_service.py
from sqlalchemy.orm import Session
from typing import Optional
from models.user import User, ProfileType
from schemas.user import UserCreate, UserLogin, UserMeDto
from schemas.post import PostDto
from models.post import Post
from models.like import Like
from datetime import datetime
from sqlalchemy import func
import bcrypt

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_with_posts(db: Session, user_id: int) -> Optional[UserMeDto]:
    """Get user by ID with their posts and related data"""
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if user is None:
        return None
    
    # Fetch posts created by this user
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    
    # Map database models to DTOs
    post_dtos = []
    for post in posts:
        # Count likes for this post
        likes_count = db.query(func.count(Like.like_id)).filter(Like.post_id == post.post_id).scalar()
        
        # Check if user liked this post
        is_liked = db.query(Like).filter(
            Like.post_id == post.post_id,
            Like.user_id == user_id
        ).first() is not None
        
        # Count comments (assuming child_id refers to parent post for comments)
        comments_count = db.query(func.count(Post.post_id)).filter(Post.child_id == post.post_id).scalar()
        
        # Format creation date as ISO string if it exists
        creation_date_str = None
        if post.creation_date:
            if isinstance(post.creation_date, datetime):
                creation_date_str = post.creation_date.isoformat()
            else:
                creation_date_str = str(post.creation_date)
        
        post_dto = PostDto(
            content=post.content,
            childId=post.child_id,
            mediaLink=post.media_link,
            postTypeId=post.post_type_id,
            postId=post.post_id,
            userId=post.user_id,
            creationDate=creation_date_str,
            viewsCount=post.views_count,
            isLiked=is_liked,
            likesCount=likes_count,
            commentsCount=comments_count
        )
        post_dtos.append(post_dto)
    
    # Create UserMeDto with posts included
    user_me_dto = UserMeDto(
        login=user.login,
        name=user.name,
        typeId=user.type_id,
        imageLink=user.image_link,
        description=user.description,
        userId=user.user_id,
        rating=user.rating,
        posts=post_dtos
    )
    
    return user_me_dto


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