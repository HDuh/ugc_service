from functools import lru_cache
from typing import Optional

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo
from models.models import Bookmark, Bookmarks


class UserService:
    """Class to interact with MongoDB about user bookmarks."""

    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo = mongo
        self.database = self.mongo.movies
        self.collection = self.database.get_collection("bookmarks")

    async def get_user_bookmarks(self, user_id: str) -> Optional[Bookmarks]:
        """Get user bookmarks by user_id"""
        films = await self.collection.find_one({"user_id": user_id})
        if not films:
            return
        bookmarks = Bookmarks(user_id=user_id, movie_ids=[])
        cursor = self.collection.find({"user_id": user_id})
        for document in await cursor.to_list(length=100):
            bookmarks.movie_ids.append(document["movie_id"])
        return bookmarks

    async def add_user_bookmark(self, user_id: str, film_id: str) -> Bookmark:
        """Add bookmark to user by film_id."""
        bookmark = await self.collection.find_one(
            {"$and": [{"movie_id": film_id}, {"user_id": user_id}]}
        )
        if bookmark:
            return Bookmark(user_id=bookmark["user_id"], movie_id=bookmark["movie_id"])
        await self.collection.insert_one({"user_id": user_id, "movie_id": film_id})
        return Bookmark(user_id=user_id, movie_id=film_id)

    async def remove_user_bookmark(self, user_id: str, film_id: str) -> Optional[Bookmark]:
        """Find and delete user bookmark by user_id and film_id."""
        bookmark = await self.collection.find_one_and_delete(
            {"$and": [{"movie_id": film_id}, {"user_id": user_id}]},
            projection={"_id": False},
        )
        if not bookmark:
            return
        return Bookmark(user_id=user_id, movie_id=film_id)


@lru_cache()
def get_user_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> UserService:
    return UserService(mongo)
