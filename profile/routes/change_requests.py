# app/routes/change_requests.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.change_request import ChangeRequest, ChangeRequestCreate
from services import change_request_service, education_program_service
from utils.auth import get_current_user, is_student, is_institution, TokenData

router = APIRouter(
    prefix="/change-requests",
    tags=["change_requests"]
)

@router.get("/", response_model=List[ChangeRequest])
def read_change_requests(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(get_current_user)
):
    change_requests = change_request_service.get_change_requests(db, skip=skip, limit=limit)
    return change_requests

@router.get("/user/{user_id}", response_model=List[ChangeRequest])
def read_user_change_requests(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(get_current_user)
):
    if str(user_id) != token_data.sub and "Institution" not in token_data.roles:
        raise HTTPException(status_code=403, detail="Not authorized to view these change requests")
    
    change_requests = change_request_service.get_change_requests_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return change_requests

@router.get("/program/{program_id}", response_model=List[ChangeRequest])
def read_program_change_requests(
    program_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_institution)
):
    # Verify that the institution owns the program
    program = education_program_service.get_education_program(db, program_id=program_id)
    if program is None:
        raise HTTPException(status_code=404, detail="Education program not found")
    if str(program.user_id) != token_data.sub:
        raise HTTPException(status_code=403, detail="Not authorized to view change requests for this program")
    
    change_requests = change_request_service.get_change_requests_by_program(db, program_id=program_id, skip=skip, limit=limit)
    return change_requests

@router.post("/", response_model=ChangeRequest)
def create_change_request(
    change_request: ChangeRequestCreate,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(is_student)
):
    # Students can create change requests
    return change_request_service.create_change_request(db=db, change_request=change_request, user_id=int(token_data.sub))

@router.delete("/{change_request_id}")
def delete_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(get_current_user)
):
    # Check if user is authorized to delete this change request
    change_request = change_request_service.get_change_request(db, change_request_id=change_request_id)
    if change_request is None:
        raise HTTPException(status_code=404, detail="Change request not found")
    
    # Allow deletion by the requestor or the institution that owns the program
    if str(change_request.from_id) != token_data.sub:
        program = education_program_service.get_education_program(db, program_id=change_request.program_id)
        if program is None or str(program.user_id) != token_data.sub:
            raise HTTPException(status_code=403, detail="Not authorized to delete this change request")
    
    change_request_service.delete_change_request(db, change_request_id=change_request_id)
    return {"detail": "Change request successfully deleted"}