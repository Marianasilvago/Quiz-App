from os import access
from fastapi import Depends, FastAPI, status, HTTPException, Response, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2


router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):

    #OAuth2PasswordRequestForm returns :
    # username 
    # password

    
    #match email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials" )

    #check if password entered matches. Look in utils.py
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid Credentials" )

        
#create a token 
    #the data is going to be the encoded payload. check oauth2
    #data ke andar you can pass any fields you want for the payload
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
#return token

    return {"access_token": access_token, "token_type": "bearer"}