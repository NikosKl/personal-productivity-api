from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.analytics import ProductivitySummary
from app.services.analytics import get_productivity_summary

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get('/summary', response_model=ProductivitySummary)
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_productivity_summary(db, current_user)
