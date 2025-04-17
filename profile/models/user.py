# app/models/user.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user_table"

    user_id = Column(BigInteger, primary_key=True, index=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    type_id = Column(BigInteger, ForeignKey("profile_type_table.type_id"), nullable=False)
    name = Column(String, nullable=False)
    image_link = Column(String, nullable=True)
    description = Column(String, nullable=True)
    rating = Column(Float, nullable=False, default=0.0)

    # Relationships
    profile_type = relationship("ProfileType", back_populates="users")
    education_programs = relationship("EducationProgram", back_populates="user")
    change_requests = relationship("ChangeRequest", back_populates="from_user")

    posts = relationship("Post", back_populates="user")
    tags = relationship("TagForUser", back_populates="user")
    likes = relationship("Like", back_populates="user")
# To:


class ProfileType(Base):
    __tablename__ = "profile_type_table"

    type_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    users = relationship("User", back_populates="profile_type")