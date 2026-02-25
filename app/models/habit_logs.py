from datetime import datetime, date
from sqlalchemy import ForeignKey, DateTime, Date, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class HabitLogs(Base):
    __tablename__ = 'habit_logs'
    __table_args__ = (UniqueConstraint('user_id', 'habit_id', 'log_date', name='uniq_user_habit_log_date'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete='CASCADE'), index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    log_date: Mapped[date] = mapped_column(Date, nullable=False)