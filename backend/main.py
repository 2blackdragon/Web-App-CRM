from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
import json

from database import create_tables, delete_tables

from repository import UserRepository, RecordRepository, AvailableDatetimeRepository

from schemas import (UserBase, UserModel, 
                    RecordBase, RecordModel, 
                    AvailableDatetimeBase, AvailableDatetimeModel) 


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("created tables")
    yield
    print("OFF")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def add_test_data_to_database():

    master1 = UserBase(name="Ирина", surname="Гусак", is_master=True)
    master2 = UserBase(name="Анастасия", surname="Гусак", is_master=True)

    client1 = UserBase(name="Иван", surname="Иванов", is_master=False)
    client2 = UserBase(name="Петр", surname="Петров", is_master=False)

    await UserRepository.add_user(master1)
    await UserRepository.add_user(master2)
    await UserRepository.add_user(client1)
    await UserRepository.add_user(client2)

    await AvailableDatetimeRepository.add_available_datetime(AvailableDatetimeBase(master_id=1, available_datetime="2024-10-08T10:15"))
    await AvailableDatetimeRepository.add_available_datetime(AvailableDatetimeBase(master_id=2, available_datetime="2024-10-08T11:15"))
    await AvailableDatetimeRepository.add_available_datetime(AvailableDatetimeBase(master_id=1, available_datetime="2024-10-08T12:15"))
    await AvailableDatetimeRepository.add_available_datetime(AvailableDatetimeBase(master_id=1, available_datetime="2024-10-09T09:20"))


async def form_available_data_to_json(id, fullname, available_datetime_list):
    available_str_datetime_list = []
    for available_datetime in available_datetime_list:
        str_available_datetime = datetime.strftime(available_datetime, "%Y-%m-%dT%H:%M")
        available_str_datetime_list.append(str_available_datetime)
    json_data = json.dumps({"master_id": id, "master_fullname": fullname, "master_available_datetime": available_str_datetime_list}, ensure_ascii=False)
    return json_data



async def get_available_datetime():
    master_id_list = await UserRepository.get_all_master_id()

    all_available_data = []
    for master_id in master_id_list:
        master_fullname = await UserRepository.get_master_fullname_by_id(master_id)
        master_available_datetime_list = await AvailableDatetimeRepository.get_master_available_datetime(master_id)
        json_available_data = await form_available_data_to_json(master_id, master_fullname, master_available_datetime_list)
        all_available_data.append(json_available_data)

    return all_available_data


@app.post("/login")
async def login_user(model: UserBase):
    #add test rows in database
    await add_test_data_to_database()
    
    await UserRepository.add_user(model)


@app.get("/")
async def show_available_datetime():

    all_available_datetime = await get_available_datetime()

    return all_available_datetime


@app.post("/add_record")
async def add_record(model: RecordBase):
    await RecordRepository.add_record(model)
    await AvailableDatetimeRepository.delete_available_datetime(AvailableDatetimeBase(master_id=model.master_id, available_datetime=model.record_datetime))


