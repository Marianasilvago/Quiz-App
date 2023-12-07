from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class QuestionBase(BaseModel):

    question: str
    choice1: str
    choice2: str
    choice3: str
    choice4: str
    correct_choice : str
    published : Optional[bool] = True
    # category: Optional[str] = None
    # difficulty: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):

    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str]= None