# app/services/change_request_service.py
from sqlalchemy.orm import Session
from models.change_request import ChangeRequest
from schemas.change_request import ChangeRequestCreate

def get_change_request(db: Session, change_request_id: int):
    return db.query(ChangeRequest).filter(ChangeRequest.change_request_id == change_request_id).first()

def get_change_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ChangeRequest).offset(skip).limit(limit).all()

def get_change_requests_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ChangeRequest).filter(ChangeRequest.from_id == user_id).offset(skip).limit(limit).all()

def get_change_requests_by_program(db: Session, program_id: int, skip: int = 0, limit: int = 100):
    return db.query(ChangeRequest).filter(ChangeRequest.program_id == program_id).offset(skip).limit(limit).all()

def create_change_request(db: Session, change_request: ChangeRequestCreate, user_id: int):
    db_change_request = ChangeRequest(**change_request.dict(), from_id=user_id)
    db.add(db_change_request)
    db.commit()
    db.refresh(db_change_request)
    return db_change_request

def delete_change_request(db: Session, change_request_id: int):
    db_change_request = get_change_request(db, change_request_id)
    if db_change_request:
        db.delete(db_change_request)
        db.commit()
    return db_change_request