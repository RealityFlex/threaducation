from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from database import Base

class Like(Base):
    __tablename__ = "like_table"
    
    like_id = Column(BigInteger, primary_key=True, index=True)
    post_id = Column(BigInteger, ForeignKey("post_table.post_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    
    # Relationships
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")