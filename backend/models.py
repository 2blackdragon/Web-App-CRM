import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class UserORM(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    is_master: Mapped[bool]


class RecordORM(Base):
    __tablename__ = "Record"

    id: Mapped[int] = mapped_column(primary_key=True)
    master_id: Mapped[int]
    client_id: Mapped[int]
    record_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    

class AvailableDatetimeORM(Base):
    __tablename__ = "AvailableDatetime"

    id: Mapped[int] = mapped_column(primary_key=True)
    master_id: Mapped[int]
    available_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
