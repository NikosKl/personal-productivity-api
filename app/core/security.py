from datetime import timezone, datetime, timedelta
import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import JWT_ALGORITHM, JWT_SECRET, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:

    to_encode = {'sub': subject}

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise InvalidTokenError()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user_id = int(payload['sub'])
        if user_id is None:
            raise InvalidTokenError()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise InvalidTokenError()
        return user
    except InvalidTokenError:
        raise InvalidTokenError()