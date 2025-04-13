# app/models/tag.py
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database import Base

class Tag(Base):
    __tablename__ = "tag_table"

    tag_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tag_type_id = Column(BigInteger, nullable=False)

    # Relationships
    user_tags = relationship("TagForUser", back_populates="tag")

class TagForUser(Base):
    __tablename__ = "tags_for_user_table"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("tag_table.tag_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="tags")
    tag = relationship("Tag", back_populates="user_tags")