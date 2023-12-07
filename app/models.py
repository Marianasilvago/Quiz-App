import sqlalchemy
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key = True, nullable = False)
    question = Column(String, nullable = False)
    choice1 = Column(String, nullable = False)
    choice2 = Column(String, nullable = False)
    choice3 = Column(String, nullable = False)
    choice4 = Column(String, nullable = False)
    correct_choice = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()') )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE" ), nullable = False)

    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()') )
