from sqlalchemy import Column, Integer, String
from database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    external_id = Column(String)
    full_name = Column(String)
    additional_info = Column(String)