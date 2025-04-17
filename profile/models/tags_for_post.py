# In models/tag.py
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from database import Base

class TagsForPost(Base):
    __tablename__ = "tags_for_post_table"
    
    id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("post_table.post_id"), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("tag_table.tag_id"), nullable=False)
    
    # Use strings only to avoid circular imports
    post = relationship("Post", back_populates="tags")
    tag = relationship("Tag", back_populates="post_tags")