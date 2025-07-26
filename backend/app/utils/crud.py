from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.database import get_async_session

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    async def get_collection(self) -> AsyncIOMotorCollection:
        db = await get_database()
        return db[self.collection_name]

    async def get(self, id: Union[str, ObjectId]) -> Optional[Dict[str, Any]]:
        collection = await self.get_collection()
        if isinstance(id, str):
            id = ObjectId(id)
        return await collection.find_one({"_id": id})

    async def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        collection = await self.get_collection()
        filter_dict = filter_dict or {}
        cursor = collection.find(filter_dict).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def create(self, obj_in: CreateSchemaType, **kwargs) -> Dict[str, Any]:
        collection = await self.get_collection()
        obj_data = obj_in.dict()
        obj_data.update(kwargs)
        
        result = await collection.insert_one(obj_data)
        created_obj = await collection.find_one({"_id": result.inserted_id})
        return created_obj

    async def update(
        self, 
        id: Union[str, ObjectId], 
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        collection = await self.get_collection()
        if isinstance(id, str):
            id = ObjectId(id)
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if update_data:
            await collection.update_one(
                {"_id": id}, 
                {"$set": update_data}
            )
        
        return await collection.find_one({"_id": id})

    async def remove(self, id: Union[str, ObjectId]) -> bool:
        collection = await self.get_collection()
        if isinstance(id, str):
            id = ObjectId(id)
        
        result = await collection.delete_one({"_id": id})
        return result.deleted_count > 0

    async def count(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        collection = await self.get_collection()
        filter_dict = filter_dict or {}
        return await collection.count_documents(filter_dict)

    async def exists(self, id: Union[str, ObjectId]) -> bool:
        collection = await self.get_collection()
        if isinstance(id, str):
            id = ObjectId(id)
        
        result = await collection.find_one({"_id": id}, {"_id": 1})
        return result is not None

    async def find_one(self, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        collection = await self.get_collection()
        return await collection.find_one(filter_dict)

    async def find_many(
        self, 
        filter_dict: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        collection = await self.get_collection()
        cursor = collection.find(filter_dict).skip(skip).limit(limit)
        
        if sort:
            cursor = cursor.sort(sort)
        
        return await cursor.to_list(length=limit)

    async def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        collection = await self.get_collection()
        cursor = collection.aggregate(pipeline)
        return await cursor.to_list(length=None)