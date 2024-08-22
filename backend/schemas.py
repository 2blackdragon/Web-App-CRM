# пока непонятно нужно ли это
from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    name: str
    surname: str
    is_master: bool


class UserModel(UserBase):
    id: int


class RecordBase(BaseModel):
    master_id: int
    client_id: int
    record_datetime: datetime.datetime


class RecordModel(RecordBase):
    id: int


class AvailableDatetimeBase(BaseModel):
    master_id: int
    available_datetime: datetime.datetime


class AvailableDatetimeModel(AvailableDatetimeBase):
    id: int