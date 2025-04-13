# app/models/change_request.py
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database import Base

class ChangeRequest(Base):
    __tablename__ = "change_request_table"

    change_request_id = Column(BigInteger, primary_key=True, index=True)
    description = Column(String, nullable=False)
    from_id = Column(BigInteger, ForeignKey("user_table.user_id"), nullable=False)
    program_id = Column(BigInteger, ForeignKey("education_program_table.program_id"), nullable=False)

    # Relationships
    from_user = relationship("User", back_populates="change_requests")
    program = relationship("EducationProgram", back_populates="change_requests")