import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import Database

# Mock database fixture for custom catalogs
class MockCustomCatalogDb:
    def __init__(self):
        self._catalogs = []
        self._order = []
        self._settings = {"enabled_keys": ["bollywood", "netflix", "anime"]}
        self._state = {}

    async def get_custom_catalogs(self, visible_only: bool = False):
        if visible_only:
            return [c for c in self._catalogs if c.get("visible", True)]
        return list(self._catalogs)

    async def get_custom_catalog(self, catalog_id: str):
        for c in self._catalogs:
            if c["_id"] == catalog_id:
                return c
        return None

    async def create_custom_catalog(self, name: str, visibility: str = "public", allowed_tokens = None):
        cid = f"cat_{len(self._catalogs) + 1}"
        cat = {
            "_id": cid,
            "name": name,
            "visibility": visibility,
            "allowed_tokens": allowed_tokens or [],
            "visible": visibility != "owner",
            "exclusive": False,
            "searchable": False,
            "items": [],
        }
        self._catalogs.append(cat)
        return cid

    async def update_custom_catalog(self, catalog_id: str, **kwargs):
        cat = await self.get_custom_catalog(catalog_id)
        if cat:
            cat.update(kwargs)
            return True
        return False

    async def delete_custom_catalog(self, catalog_id: str):
        before = len(self._catalogs)
        self._catalogs = [c for c in self._catalogs if c["_id"] != catalog_id]
        return len(self._catalogs) < before

    async def add_item_to_custom_catalog(self, catalog_id: str, item: dict):
        cat = await self.get_custom_catalog(catalog_id)
        if cat:
            cat["items"].append(item)
            return True
        return False

    async def remove_item_from_custom_catalog(self, catalog_id: str, tmdb_id: int, media_type: str):
        cat = await self.get_custom_catalog(catalog_id)
        if cat:
            cat["items"] = [it for it in cat["items"] if not (it["tmdb_id"] == tmdb_id and it["media_type"] == media_type)]
            return True
        return False

    async def get_catalog_order(self):
        return list(self._order)

    async def save_catalog_order(self, order):
        self._order = list(order)

    async def get_settings(self):
        return {"tmdb_api_key": "test_key"}


@pytest.mark.asyncio
async def test_custom_catalogs_api_crud():
    mock_db = MockCustomCatalogDb()
    app.state.db = mock_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create catalog
        create_res = await client.post("/api/custom-catalogs", json={"name": "Marvel Collection", "visibility": "public"})
        assert create_res.status_code == 200
        cat_data = create_res.json()["catalog"]
        cat_id = cat_data["_id"]
        assert cat_data["name"] == "Marvel Collection"

        # 2. List catalogs
        list_res = await client.get("/api/custom-catalogs")
        assert list_res.status_code == 200
        cats = list_res.json()["catalogs"]
        assert len(cats) == 1
        assert cats[0]["_id"] == cat_id

        # 3. Add item
        add_item_res = await client.post(
            f"/api/custom-catalogs/{cat_id}/items",
            json={"tmdb_id": 299536, "title": "Avengers: Infinity War", "media_type": "movie"}
        )
        assert add_item_res.status_code == 200
        assert add_item_res.json()["added"] is True

        # 4. Get items
        items_res = await client.get(f"/api/custom-catalogs/{cat_id}/items")
        assert items_res.status_code == 200
        items = items_res.json()["items"]
        assert len(items) == 1
        assert items[0]["tmdb_id"] == 299536

        # 5. Check manifest has the custom catalog
        manifest_res = await client.get("/test_token/manifest.json")
        assert manifest_res.status_code == 200
        manifest = manifest_res.json()
        cat_ids = [c["id"] for c in manifest["catalogs"]]
        assert f"custom_{cat_id}" in cat_ids
