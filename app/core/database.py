import time
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from app.indexer.pipeline import UnmatchedItem
from app.stremio.catalog import LibraryMediaItem


class Database:
    def __init__(self, uri: str, db_name: str = "telegram_stremio_v2"):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
        self.db: AsyncIOMotorDatabase = self.client[db_name]

    @property
    def media(self):
        return self.db["media"]

    @property
    def unmatched(self):
        return self.db["unmatched_queue"]

    @property
    def tokens(self):
        return self.db["tokens"]

    @property
    def watch_history(self):
        return self.db["watch_history"]

    @property
    def settings(self):
        return self.db["settings"]

    @property
    def custom_catalogs(self):
        return self.db["custom_catalogs"]

    async def init_indexes(self) -> None:
        """Create clean, conflict-proof indexes."""
        # 1. Media collection
        await self.media.create_index([("tmdb_id", ASCENDING), ("media_type", ASCENDING)])
        await self.media.create_index([("chat_id", ASCENDING), ("message_id", ASCENDING)], unique=True)
        await self.media.create_index([("title", "text"), ("matched_alias", "text")])

        # 2. Unmatched queue
        await self.unmatched.create_index([("chat_id", ASCENDING), ("message_id", ASCENDING)], unique=True)
        await self.unmatched.create_index([("created_at", DESCENDING)])

        # 3. User tokens
        await self.tokens.create_index([("token", ASCENDING)], unique=True)

        # 4. Watch history
        await self.watch_history.create_index([("token", ASCENDING), ("watched_at", DESCENDING)])

    async def save_media(self, media_record: Dict[str, Any]) -> None:
        record = dict(media_record)
        record["updated_at"] = time.time()
        await self.media.update_one(
            {"chat_id": record["chat_id"], "message_id": record["message_id"]},
            {"$set": record},
            upsert=True,
        )

    async def save_unmatched(self, item: UnmatchedItem) -> str:
        doc = {
            "chat_id": item.chat_id,
            "message_id": item.message_id,
            "filename": item.filename,
            "caption": item.caption,
            "file_id": item.file_id,
            "file_size": item.file_size,
            "parsed_title": item.parsed_title,
            "parsed_year": item.parsed_year,
            "quality": item.quality,
            "created_at": time.time(),
        }
        res = await self.unmatched.update_one(
            {"chat_id": item.chat_id, "message_id": item.message_id},
            {"$set": doc},
            upsert=True,
        )
        if res.upserted_id:
            return str(res.upserted_id)
        existing = await self.unmatched.find_one({"chat_id": item.chat_id, "message_id": item.message_id})
        return str(existing["_id"]) if existing else "unknown"

    async def get_unmatched(self, item_id: str) -> Optional[UnmatchedItem]:
        from bson import ObjectId
        try:
            doc = await self.unmatched.find_one({"_id": ObjectId(item_id)})
        except Exception:
            return None
        if not doc:
            return None
        return UnmatchedItem(
            id=str(doc["_id"]),
            chat_id=doc["chat_id"],
            message_id=doc["message_id"],
            filename=doc.get("filename", ""),
            caption=doc.get("caption"),
            file_id=doc.get("file_id", ""),
            file_size=doc.get("file_size", 0),
            parsed_title=doc.get("parsed_title", ""),
            parsed_year=doc.get("parsed_year"),
            quality=doc.get("quality"),
        )

    async def list_unmatched(self, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.unmatched.find().sort("created_at", DESCENDING).limit(limit)
        results = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            results.append(doc)
        return results

    async def remove_unmatched(self, item_id: str) -> None:
        from bson import ObjectId
        try:
            await self.unmatched.delete_one({"_id": ObjectId(item_id)})
        except Exception:
            pass

    async def get_library_items(self) -> List[LibraryMediaItem]:
        cursor = self.media.find().sort("updated_at", DESCENDING)
        items = []
        async for doc in cursor:
            items.append(
                LibraryMediaItem(
                    tmdb_id=doc.get("tmdb_id", 0),
                    title=doc.get("title", ""),
                    year=doc.get("year"),
                    media_type=doc.get("media_type", "movie"),
                    poster_url=doc.get("poster_url"),
                    file_id=doc.get("file_id", ""),
                    quality=doc.get("quality"),
                    season=doc.get("season"),
                    episode=doc.get("episode"),
                )
            )
        return items

    async def log_watch(self, token: str, tmdb_id: int, title: str, media_type: str) -> None:
        await self.watch_history.insert_one({
            "token": token,
            "tmdb_id": tmdb_id,
            "title": title,
            "media_type": media_type,
            "watched_at": time.time(),
        })

    async def get_recently_watched_ids(self, token: str, limit: int = 5) -> List[int]:
        cursor = self.watch_history.find({"token": token}).sort("watched_at", DESCENDING).limit(limit)
        ids = []
        async for doc in cursor:
            if doc.get("tmdb_id") and doc["tmdb_id"] not in ids:
                ids.append(doc["tmdb_id"])
        return ids

    async def get_settings(self) -> Optional[Dict[str, Any]]:
        doc = await self.settings.find_one({"_id": "app_settings"})
        if not doc:
            return None
        doc.pop("_id", None)
        return doc

    async def save_settings(self, settings_data: Dict[str, Any]) -> None:
        data = dict(settings_data)
        data["updated_at"] = time.time()
        await self.settings.update_one(
            {"_id": "app_settings"},
            {"$set": data},
            upsert=True,
        )

    async def get_custom_catalogs(self, visible_only: bool = False) -> List[Dict[str, Any]]:
        query = {"visible": True} if visible_only else {}
        cursor = self.custom_catalogs.find(query).sort("updated_at", DESCENDING)
        catalogs = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            catalogs.append(doc)
        return catalogs

    async def get_custom_catalog(self, catalog_id: str) -> Optional[Dict[str, Any]]:
        from bson import ObjectId
        try:
            doc = await self.custom_catalogs.find_one({"_id": ObjectId(catalog_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
                return doc
        except Exception:
            pass
        return None

    async def create_custom_catalog(self, name: str, visibility: str = "public", allowed_tokens: Optional[List[str]] = None) -> str:
        doc = {
            "name": name.strip(),
            "visibility": visibility,
            "allowed_tokens": allowed_tokens or [],
            "visible": visibility != "owner",
            "exclusive": False,
            "searchable": False,
            "items": [],
            "created_at": time.time(),
            "updated_at": time.time(),
        }
        res = await self.custom_catalogs.insert_one(doc)
        return str(res.inserted_id)

    async def update_custom_catalog(self, catalog_id: str, **kwargs) -> bool:
        from bson import ObjectId
        kwargs["updated_at"] = time.time()
        if "visibility" in kwargs:
            kwargs["visible"] = kwargs["visibility"] != "owner"
        res = await self.custom_catalogs.update_one({"_id": ObjectId(catalog_id)}, {"$set": kwargs})
        return res.modified_count > 0

    async def delete_custom_catalog(self, catalog_id: str) -> bool:
        from bson import ObjectId
        res = await self.custom_catalogs.delete_one({"_id": ObjectId(catalog_id)})
        return res.deleted_count > 0

    async def add_item_to_custom_catalog(self, catalog_id: str, item: Dict[str, Any]) -> bool:
        from bson import ObjectId
        res = await self.custom_catalogs.update_one(
            {
                "_id": ObjectId(catalog_id),
                "items": {"$not": {"$elemMatch": {"tmdb_id": item["tmdb_id"], "media_type": item["media_type"]}}},
            },
            {
                "$push": {"items": {"$each": [item], "$position": 0}},
                "$set": {"updated_at": time.time()},
            },
        )
        return res.modified_count > 0

    async def remove_item_from_custom_catalog(self, catalog_id: str, tmdb_id: int, media_type: str) -> bool:
        from bson import ObjectId
        res = await self.custom_catalogs.update_one(
            {"_id": ObjectId(catalog_id)},
            {
                "$pull": {"items": {"tmdb_id": tmdb_id, "media_type": media_type}},
                "$set": {"updated_at": time.time()},
            },
        )
        return res.modified_count > 0

    async def get_catalog_order(self) -> List[str]:
        doc = await self.db["state"].find_one({"_id": "catalog_order"})
        return (doc.get("order") if doc else []) or []

    async def save_catalog_order(self, order: List[str]) -> None:
        await self.db["state"].update_one(
            {"_id": "catalog_order"},
            {"$set": {"order": order, "updated_at": time.time()}},
            upsert=True,
        )
