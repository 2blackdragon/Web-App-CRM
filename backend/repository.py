from sqlalchemy import select, delete

import datetime

from database import async_session

from models import UserORM, RecordORM, AvailableDatetimeORM

from schemas import (UserBase, UserModel, 
                    RecordBase, RecordModel, 
                    AvailableDatetimeBase, AvailableDatetimeModel) 


class UserRepository:
    @classmethod
    async def check_uniq_user(cls, user_model) -> bool:
        async with async_session() as session:
            query = select(UserORM.id).where((UserORM.name == user_model.name) & 
                                             (UserORM.surname == user_model.surname) &
                                             (UserORM.is_master == user_model.is_master))
            response = await session.execute(query)
            response = response.scalars().first()
            if response:
                return False
            return True
        
    @classmethod
    async def add_user(cls, user_model) -> int:
        async with async_session() as session:
            unique = await UserRepository.check_uniq_user(user_model)
            if unique:
                item_to_add = UserORM(name=user_model.name,
                                    surname=user_model.surname,
                                    is_master=user_model.is_master)
                session.add(item_to_add)
                await session.commit()

    @classmethod
    async def get_user_id(cls, user_model) -> int:
        async with async_session() as session:
            query = select(UserORM.id).where((UserORM.name == user_model.name) &
                                             (UserORM.surname == user_model.surname) &
                                             (UserORM.is_master == user_model.is_master))
            user_id = await session.execute(query)
            user_id = user_id.scalars().first()
            return user_id
    
    @classmethod
    async def get_all_master_id(cls) -> list[int]:
        async with async_session() as session:
            query = select(UserORM.id).where(UserORM.is_master == 1).distinct()
            master_id_list = await session.execute(query)
            master_id_list = master_id_list.scalars().all()
            return master_id_list
    
    @classmethod
    async def get_master_fullname_by_id(cls, master_id) -> str:
        async with async_session() as session:
            query = select(UserORM).where(UserORM.id == master_id)
            master_model = await session.execute(query)
            master_model = master_model.scalars().first()
            return f"{master_model.name} {master_model.surname}"


class RecordRepository:
    @classmethod
    async def check_uniq_record(cls, record_model) -> bool:
        async with async_session() as session:
            query = select(RecordORM.id).where((RecordORM.master_id == record_model.master_id) & 
                                             (RecordORM.client_id == record_model.client_id) &
                                             (RecordORM.record_datetime == record_model.record_datetime))
            response = await session.execute(query)
            response = response.scalars().first()
            if response:
                return False
            return True

    @classmethod
    async def add_record(cls, record_model):
        async with async_session() as session:
            unique = await RecordRepository.check_uniq_record(record_model)
            if unique:
                item_to_add = RecordORM(master_id=record_model.master_id, 
                                        client_id=record_model.client_id, 
                                        record_datetime=record_model.record_datetime)
                session.add(item_to_add)
                await session.commit()


class AvailableDatetimeRepository:
    @classmethod
    async def check_uniq_available_datetime(cls, available_datetime_model) -> bool:
        async with async_session() as session:
            query = select(AvailableDatetimeORM.id).where((AvailableDatetimeORM.master_id == available_datetime_model.master_id) & 
                                                          (AvailableDatetimeORM.available_datetime == available_datetime_model.available_datetime))
            response = await session.execute(query)
            response = response.scalars().first()
            if response:
                return False
            return True
        
    @classmethod
    async def get_all_available_datetime(cls) -> list[RecordModel]:
        async with async_session() as session:
            query = select(AvailableDatetimeORM).order_by(AvailableDatetimeORM.master_id, AvailableDatetimeORM.available_datetime)
            available_datetime_list = await session.execute(query)
            available_datetime_list = available_datetime_list.scalars().all()
            return available_datetime_list
    

    @classmethod
    async def get_master_available_datetime(cls, master_id) -> list[datetime.datetime]:
        async with async_session() as session:
            query = select(AvailableDatetimeORM.available_datetime).where(AvailableDatetimeORM.master_id == master_id).order_by(AvailableDatetimeORM.available_datetime)
            available_datetime_list = await session.execute(query)
            available_datetime_list = available_datetime_list.scalars().all()
            return available_datetime_list
        
    @classmethod
    async def add_available_datetime(cls, available_datetime_model):
        async with async_session() as session:
            unique = await AvailableDatetimeRepository.check_uniq_available_datetime(available_datetime_model)
            if unique:
                item_to_add = AvailableDatetimeORM(master_id=available_datetime_model.master_id, 
                                                available_datetime=available_datetime_model.available_datetime)
                session.add(item_to_add)
                await session.commit()
    
    @classmethod
    async def delete_available_datetime(cls, model):
        async with async_session() as session:
            query = delete(AvailableDatetimeORM).where((AvailableDatetimeORM.master_id == model.master_id) &
                                                       (AvailableDatetimeORM.available_datetime == model.available_datetime))
            await session.execute(query)
            await session.commit()
