from fastapi import APIRouter, Depends
from .schema import UserCreate
from api.models.db import get_db
from api.models.models import User
from sqlalchemy.orm import Session

user_router = APIRouter(
    tags=['User Registration']
)


@user_router.post('/register', status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": "User registered successfully"}
