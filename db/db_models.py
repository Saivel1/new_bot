from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pass


class PaymentData(Base):
    __tablename__ = 'payment_data'

    payment_id: Mapped[str] = mapped_column(index=True)
    user_id: Mapped[str]
    status: Mapped[str] = mapped_column(server_default='pending')
    amount: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    applied: Mapped[bool] = mapped_column(default=False)


class UserOrm(Base):
    __tablename__ = "user"

    user_id: Mapped[str]
    username: Mapped[str | None]
    trial_used: Mapped[bool] = mapped_column(default=False)
    subscription_end: Mapped[datetime | None]