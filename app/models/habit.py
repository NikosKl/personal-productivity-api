from datetime import UTC, datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Habits(Base):
    __tablename__ = 'habits'

    id: Mapped[int] = mapped_column(primary_key=True )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=False)