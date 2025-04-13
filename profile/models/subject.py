# app/models/subject.py
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from database import Base

class Subject(Base):
    __tablename__ = "subject_table"

    subject_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(BigInteger, nullable=False)  # This seems to be a BigInteger in your schema, but might be a mistake?

    # Relationships
    learning_plans = relationship("LearningPlan", back_populates="subject")