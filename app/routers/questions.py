from fastapi import Depends, FastAPI, status, HTTPException, Response, APIRouter
from typing import List, Optional

from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix='/questions',
    tags= ['Questions']
)

@router.get("/", response_model=List[schemas.Question])
def get_questions(db: Session = Depends(get_db), limit: int = 5, skip: int =0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM questions""")
    # questions = cursor.fetchall()
    questions = db.query(models.Question).filter(models.Question.question.contains(search)).limit(limit).offset(skip).all()
    return questions

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Question)
def create_question(question : schemas.QuestionCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_question = models.Question(owner_id = current_user.id, **question.dict())

    db.add(new_question)
    db.commit()
    db.refresh(new_question)
                
    return new_question

@router.get("/{id}", response_model=schemas.Question)
def get_quesion(id: int, db: Session = Depends(get_db)):
    
    question = db.query(models.Question).filter(models.Question.id == id).first()
    
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Question with id {id} was not found." )

    return question


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_question(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    question_query = db.query(models.Question).filter(models.Question.id == id)
    question = question_query.first()

    if question == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with id {id} was not found.")

    if question.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    question_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Question)
def update_question(id: int, updated_question : schemas.QuestionCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    question_query = db.query(models.Question).filter(models.Question.id == id)
    question = question_query.first()

    if question == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with id {id} was not found.")

    if question.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")

    question_query.update(updated_question.dict(), synchronize_session=False)

    db.commit()

    return question_query.first()
