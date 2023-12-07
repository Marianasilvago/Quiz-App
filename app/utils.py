from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):

    #to verify password, hash the password entered and match the hash with the hash stored in the database
    return pwd_context.verify(plain_password, hashed_password)