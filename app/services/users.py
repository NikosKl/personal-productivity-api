from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.securities import hash_password, verify_password

class UserAlreadyExistsError(Exception):
    """ Raised when the user already exists """
    pass

class InvalidCredentialsError(Exception):
    """ Raised when the credentials are invalid"""
    pass

def create_user(db: Session, email: str, password: str) -> User:
    hashed_password = hash_password(password)

    user = User(
        email=email,
        hashed_password=hashed_password,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError('Email already registered')
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise InvalidCredentialsError("Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid credentials")

    return user