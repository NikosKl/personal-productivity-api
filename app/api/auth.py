from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.services.users import create_user, UserAlreadyExistsError

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(
            db,
            email=user.email,
            password=user.password)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return created_user

