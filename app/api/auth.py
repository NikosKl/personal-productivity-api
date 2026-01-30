from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.services.users import create_user, UserAlreadyExistsError, authenticate_user, InvalidCredentialsError

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(
            db,
            email=user.email,
            password=user.password)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail='Email already registered')

    return created_user

@router.post('/login', response_model=UserRead)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        authenticated_user = authenticate_user(
            db,
            email=user.email,
            password=user.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail='Invalid credentials')

    return authenticated_user