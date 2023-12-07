from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

from app import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')
#tokenurl is the login endpoint of the api with the slash removed

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    #data is the data you want to provide to the payload. That data is going to be of 
    # of type dict. We make a copy of the data , so as to preserve the original data.
    ##this data comes from auth.py

    to_encode = data.copy()

    #set expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #add the expiration time to the to_encode ki dictionary
    to_encode.update({"exp": expire})

    #encode to_encode
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM )

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):

    '''
    We can pass this as a dependency in anyone of our path operations.
    When we do that, it is going to take the token from the request automatically,
    extract the id, it is going to call 'verify_access_token' (jo humne upar banaya hai), 
    Then if we want to, we can have it automatically fetch the user from the database and add it as a parameter in our path operation function. 
    '''
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",
    headers={"WW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    '''
    this is used for specific endpoints thst should be protected.
    eg: if to create a post, users need to be logged in.
    so we add in an extra dependency in the path operation function

    eg in create_questions() function:
    def create_question(question : schemas.QuestionCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user))

    the  user_id: int = Depends(oauth2.get_current_user) is the dependency added.
    '''
    return user
 

