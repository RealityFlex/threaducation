# app/models/education_program.py
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database import Base

class EducationProgram(Base):
    __tablename__ = "education_program_table"

    program_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    code = Column(BigInteger, nullable=False)
    name = Column(BigInteger, nullable=False)  # This seems to be a BigInteger in your schema, but might be a mistake?
    time = Column(BigInteger, nullable=False)
    education_type_id = Column(BigInteger, ForeignKey("education_type_table.education_type_id"), nullable=False)
    description = Column(String, nullable=False)
    quota = Column(BigInteger, nullable=False)

    # Relationships
    user = relationship("User", back_populates="education_programs")
    education_type = relationship("EducationType", back_populates="programs")
    learning_plans = relationship("LearningPlan", back_populates="program")
    change_requests = relationship("ChangeRequest", back_populates="program")

class EducationType(Base):
    __tablename__ = "education_type_table"

    education_type_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    programs = relationship("EducationProgram", back_populates="education_type")

class LearningPlan(Base):
    __tablename__ = "learning_plan_table"

    id = Column(BigInteger, primary_key=True, index=True)
    program_id = Column(BigInteger, ForeignKey("education_program_table.program_id"), nullable=False)
    subject_id = Column(BigInteger, ForeignKey("subject_table.subject_id"), nullable=False)
    hours = Column(BigInteger, nullable=False)
    semester = Column(BigInteger, nullable=False)

    # Relationships
    program = relationship("EducationProgram", back_populates="learning_plans")
    subject = relationship("Subject", back_populates="learning_plans")