from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import questions, users, auth
from .config import settings

# we remove it as we already have alembic making tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#include the routes
app.include_router(questions.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return{"message": "Welcome to My API"}


