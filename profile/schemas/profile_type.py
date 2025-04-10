from pydantic import BaseModel


class ProfileTypeBase(BaseModel):
    name: str


class ProfileTypeCreate(ProfileTypeBase):
    pass


class ProfileTypeResponse(ProfileTypeBase):
    type_id: int
    
    class Config:
        orm_mode = True