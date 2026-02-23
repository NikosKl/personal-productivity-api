from datetime import datetime, UTC
from sqlalchemy import ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HabitLogs(Base):
    __tablename__ = 'habit_logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    log_date: Mapped[Date] = mapped_column(Date, nullable=False)