from sqlalchemy import Column, Integer, String, Float, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import date

class User(Base):
    __tablename__ = "user_table"
    
    user_id = Column(BigInteger, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    type_id = Column(BigInteger, ForeignKey("profile_type_table.type_id"))
    name = Column(String)
    image_link = Column(String, nullable=True)
    description = Column(String, nullable=True)
    rating = Column(Float, default=0.0)

class ProfileType(Base):
    __tablename__ = "profile_type_table"
    
    type_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)

class Tag(Base):
    __tablename__ = "tag_table"
    
    tag_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    tag_type_id = Column(BigInteger, ForeignKey("tag_type_table.tag_type_id"))

class TagType(Base):
    __tablename__ = "tag_type_table"
    
    tag_type_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)

class TagsForUser(Base):
    __tablename__ = "tags_for_user_table"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"))
    tag_id = Column(BigInteger, ForeignKey("tag_table.tag_id"))

class Post(Base):
    __tablename__ = "post_table"
    
    post_id = Column(BigInteger, primary_key=True, index=True)
    content = Column(String)
    child_id = Column(BigInteger, nullable=True)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"))
    media_link = Column(String, nullable=True)
    creation_date = Column(Date, default=date.today)
    views_count = Column(BigInteger, default=0)
    post_type_id = Column(BigInteger, ForeignKey("post_type_table.post_type_id"))

class PostType(Base):
    __tablename__ = "post_type_table"
    
    post_type_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)

class TagsForPost(Base):
    __tablename__ = "tags_for_post_table"
    
    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("post_table.post_id"))
    tag_id = Column(BigInteger, ForeignKey("tag_table.tag_id"))

class Like(Base):
    __tablename__ = "like_table"
    
    like_id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("post_table.post_id"))
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"))