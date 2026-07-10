from datetime import datetime
from enum import Enum
from typing import List, Optional
from database import db

from flask_login import UserMixin
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


# <----------------------- Enums ----------------------->
class Role(Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    TREKKER = "Trekker"


class Difficulty(Enum):
    EASY = "Easy"
    MODERATE = "Moderate"
    HARD = "Hard"


class TrekStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    OPEN = "Open"
    CLOSED = "Closed"
    COMPLETED = "Completed"


class BookingStatus(Enum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


# <----------------------- Models ----------------------->
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role), default=Role.TREKKER)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contact_details: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    is_approved: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")
    assigned_treks: Mapped[List["Trek"]] = relationship(back_populates="staff_member")


class Trek(db.Model):
    __tablename__ = "trek"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(SAEnum(Difficulty))
    duration: Mapped[int]
    available_slots: Mapped[int]
    status: Mapped[TrekStatus] = mapped_column(
        SAEnum(TrekStatus), default=TrekStatus.PENDING
    )

    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    staff_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )

    staff_member: Mapped[Optional["User"]] = relationship(
        back_populates="assigned_treks"
    )
    bookings: Mapped[List["Booking"]] = relationship(back_populates="trek")


class Booking(db.Model):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    trek_id: Mapped[int] = mapped_column(ForeignKey("trek.id"))
    booking_date: Mapped[datetime] = mapped_column(default=datetime.now)
    status: Mapped[BookingStatus] = mapped_column(
        SAEnum(BookingStatus), default=BookingStatus.BOOKED
    )

    user: Mapped["User"] = relationship(back_populates="bookings")
    trek: Mapped["Trek"] = relationship(back_populates="bookings")
