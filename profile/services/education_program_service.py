# app/services/education_program_service.py
from sqlalchemy.orm import Session
from models.education_program import EducationProgram, EducationType, LearningPlan
from schemas.education_program import EducationProgramCreate, EducationTypeCreate, LearningPlanCreate

def get_education_program(db: Session, program_id: int):
    return db.query(EducationProgram).filter(EducationProgram.program_id == program_id).first()

def get_education_programs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EducationProgram).offset(skip).limit(limit).all()

def get_education_programs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(EducationProgram).filter(EducationProgram.user_id == user_id).offset(skip).limit(limit).all()

def create_education_program(db: Session, program: EducationProgramCreate, user_id: int):
    db_program = EducationProgram(**program.dict(), user_id=user_id)
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def update_education_program(db: Session, program_id: int, program_data: dict):
    db_program = get_education_program(db, program_id)
    if db_program:
        for key, value in program_data.items():
            setattr(db_program, key, value)
        db.commit()
        db.refresh(db_program)
    return db_program

def delete_education_program(db: Session, program_id: int):
    db_program = get_education_program(db, program_id)
    if db_program:
        db.delete(db_program)
        db.commit()
    return db_program

def get_education_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EducationType).offset(skip).limit(limit).all()

def create_education_type(db: Session, education_type: EducationTypeCreate):
    db_education_type = EducationType(**education_type.dict())
    db.add(db_education_type)
    db.commit()
    db.refresh(db_education_type)
    return db_education_type

def get_learning_plans(db: Session, program_id: int, skip: int = 0, limit: int = 100):
    return db.query(LearningPlan).filter(LearningPlan.program_id == program_id).offset(skip).limit(limit).all()

def create_learning_plan(db: Session, learning_plan: LearningPlanCreate):
    db_learning_plan = LearningPlan(**learning_plan.dict())
    db.add(db_learning_plan)
    db.commit()
    db.refresh(db_learning_plan)
    return db_learning_plan

def delete_learning_plan(db: Session, plan_id: int):
    db_learning_plan = db.query(LearningPlan).filter(LearningPlan.id == plan_id).first()
    if db_learning_plan:
        db.delete(db_learning_plan)
        db.commit()
    return db_learning_plan