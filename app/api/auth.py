from fastapi import APIRouter, Depends, HTTPException
from app.core.security import create_access_token, get_current_user
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.services.users import create_user, UserAlreadyExistsError, authenticate_user, InvalidCredentialsError

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/register', response_model=UserRead)
def register_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(
            db,
            email=user.email,
            password=user.password)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail='Email already registered')

    return created_user

@router.post('/login', response_model=Token)
def login_user_route(user: UserLogin, db: Session = Depends(get_db)):
    try:
        authenticated_user = authenticate_user(
            db,
            email=user.email,
            password=user.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail='Invalid credentials')

    access_token = create_access_token(subject= str(authenticated_user.id))
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/me', response_model=UserRead)
def read_user(current_user: User = Depends(get_current_user)):
    return current_user