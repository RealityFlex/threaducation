from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from database import Base

class TagsForUser(Base):
    __tablename__ = "tags_for_user_table"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("tag_table.tag_id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="tags")
    tag = relationship("Tag", back_populates="user_tags")