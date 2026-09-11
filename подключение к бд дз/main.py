from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import User as UserModel


Base.metadata.create_all(bind=engine)


app = FastAPI()


class User(BaseModel):
    name : str
    age: int
    email: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()