from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from sqlalchemy.orm import Session

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)

class UserAlreadyExistsError(Exception):
    """ Raised when the user already exists """
    pass

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

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