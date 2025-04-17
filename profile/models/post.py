# In models/post.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import relationship
from database import Base

# Import the tag models - make sure this works with your directory structure
from models.tags_for_post import TagsForPost  # Import the actual class

class Post(Base):
    __tablename__ = "post_table"
    
    post_id = Column(BigInteger, primary_key=True, index=True)
    content = Column(String, nullable=False)
    child_id = Column(BigInteger, ForeignKey("post_table.post_id"), nullable=True)  # Добавлен ForeignKey
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    media_link = Column(String, nullable=True)
    creation_date = Column(Date, nullable=False)
    views_count = Column(BigInteger, nullable=False)
    post_type_id = Column(BigInteger, ForeignKey("post_type_table.post_type_id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="posts")
    post_type = relationship("PostType", back_populates="posts")
    likes = relationship("Like", back_populates="post")
    
    # Using the imported class
    tags = relationship("TagsForPost", back_populates="post")
    likes = relationship("Like", back_populates="post")
    
    # Self-referential relationship for comments
    parent = relationship(
        "Post",
        remote_side=[post_id],  # Указываем, что это родительская сторона
        back_populates="child_posts"
    )
    child_posts = relationship(
        "Post",
        back_populates="parent",
        foreign_keys=[child_id]  # Явно указываем внешний ключ
    )

class PostType(Base):
    __tablename__ = "post_type_table"
    
    post_type_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # Relationships
    posts = relationship("Post", back_populates="post_type")