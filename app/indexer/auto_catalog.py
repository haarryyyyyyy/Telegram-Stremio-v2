import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple, Any
import httpx

logger = logging.getLogger("auto_catalog")

AUTO_CATALOG_REGION = "IN"
AUTO_SYNC_CONCURRENCY = 5

AUTO_CATALOG_DEFINITIONS = [
    {"key": "bollywood", "name": "Bollywood", "group": "Language"},
    {"key": "hollywood", "name": "Hollywood", "group": "Language"},
    {"key": "anime", "name": "Anime", "group": "Language"},
    {"key": "kdrama", "name": "K-Drama", "group": "Language"},
    {"key": "bengali", "name": "Bengali", "group": "Language"},
    {"key": "south_indian", "name": "South Indian", "group": "Language"},
    {"key": "tamil", "name": "Tamil", "group": "Language"},
    {"key": "telugu", "name": "Telugu", "group": "Language"},
    {"key": "malayalam", "name": "Malayalam", "group": "Language"},
    {"key": "kannada", "name": "Kannada", "group": "Language"},
    {"key": "japanese", "name": "Japanese", "group": "Language"},
    {"key": "korean", "name": "Korean", "group": "Language"},

    {"key": "top_rated", "name": "Top Rated", "group": "Smart"},
    {"key": "recently_added", "name": "Recently Added", "group": "Smart"},

    {"key": "netflix", "name": "Netflix", "group": "OTT"},
    {"key": "prime_video", "name": "Prime Video", "group": "OTT"},
    {"key": "hotstar", "name": "Hotstar", "group": "OTT"},
    {"key": "apple_tv", "name": "Apple TV", "group": "OTT"},
    {"key": "hulu", "name": "Hulu", "group": "OTT"},
    {"key": "hbo", "name": "HBO", "group": "OTT"},
    {"key": "jiocinema", "name": "JioCinema", "group": "OTT"},
    {"key": "zee5", "name": "ZEE5", "group": "OTT"},
    {"key": "sonyliv", "name": "SonyLIV", "group": "OTT"},
    {"key": "mx_player", "name": "MX Player", "group": "OTT"},
    {"key": "crunchyroll", "name": "Crunchyroll", "group": "OTT"},
]

CATALOG_BY_KEY = {item["key"]: item for item in AUTO_CATALOG_DEFINITIONS}

_LANGUAGE_CATALOGS = {
    "hi": ["Bollywood"],
    "en": ["Hollywood"],
    "ja": ["Japanese"],
    "ko": ["Korean"],
    "bn": ["Bengali"],
    "te": ["South Indian", "Telugu"],
    "ta": ["South Indian", "Tamil"],
    "ml": ["South Indian", "Malayalam"],
    "kn": ["South Indian", "Kannada"],
}

_PROVIDER_ALIASES = {
    "netflix": "Netflix",
    "amazon prime video": "Prime Video",
    "prime video": "Prime Video",
    "amazon video": "Prime Video",
    "hotstar": "Hotstar",
    "disney plus hotstar": "Hotstar",
    "disney+ hotstar": "Hotstar",
    "jiohotstar": "Hotstar",
    "hulu": "Hulu",
    "apple tv": "Apple TV",
    "apple tv plus": "Apple TV",
    "apple tv+": "Apple TV",
    "hbo max": "HBO",
    "max": "HBO",
    "jio cinema": "JioCinema",
    "jiocinema": "JioCinema",
    "zee5": "ZEE5",
    "sony liv": "SonyLIV",
    "sonyliv": "SonyLIV",
    "mx player": "MX Player",
    "crunchyroll": "Crunchyroll",
}

_auto_sync_lock = asyncio.Lock()
_auto_sync_task: Optional[asyncio.Task] = None


def _catalog_key(name: str) -> str:
    value = (name or "").strip().lower().replace("&", "and")
    value = "_".join(value.split())
    value = "".join(ch for ch in value if ch.isalnum() or ch == "_")
    return f"auto_{value}"


def _doc_item(doc: dict) -> dict:
    return {
        "tmdb_id": int(doc.get("tmdb_id", 0)),
        "media_type": "series" if doc.get("media_type") in ["tv", "series", "anime"] else "movie",
        "title": doc.get("title", ""),
        "poster": doc.get("poster_url"),
        "year": doc.get("year"),
        "rating": doc.get("rating"),
        "added_at": datetime.now(timezone.utc).timestamp(),
        "visibility": doc.get("visibility") or "public",
        "allowed_tokens": doc.get("allowed_tokens") or [],
    }


def _provider_bucket(provider_name: str) -> Optional[str]:
    val = (provider_name or "").strip().lower()
    if not val:
        return None
    for needle, bucket in _PROVIDER_ALIASES.items():
        if needle in val:
            return bucket
    return None


def _extract_provider_names(watch_data: dict) -> List[str]:
    results = (watch_data or {}).get("results") or {}
    region_data = results.get(AUTO_CATALOG_REGION) or results.get("US") or {}
    names: List[str] = []
    for group in ["flatrate", "ads", "free", "rent", "buy"]:
        for p in region_data.get(group, []) or []:
            if p.get("provider_name"):
                names.append(p["provider_name"])
    return names


def classify_media_from_tmdb(doc: dict, details: dict, watch_data: dict, enabled_names: Set[str]) -> dict:
    tags: Set[str] = set()
    providers: Set[str] = set()

    media_type = "series" if doc.get("media_type") in ["tv", "series", "anime"] else "movie"
    orig_lang = details.get("original_language") or doc.get("original_language") or ""

    if doc.get("media_type") == "anime":
        tags.add("Anime")

    origin_country = details.get("origin_country") or doc.get("origin_country") or []
    production_countries = [
        c.get("iso_3166_1")
        for c in (details.get("production_countries") or [])
        if c.get("iso_3166_1")
    ] or (doc.get("production_countries") or [])

    for tag in _LANGUAGE_CATALOGS.get(orig_lang, []):
        tags.add(tag)

    if orig_lang == "hi" and ("IN" in origin_country or "IN" in production_countries or not origin_country):
        tags.add("Bollywood")

    if orig_lang == "ko" and media_type == "series":
        tags.add("K-Drama")

    genre_names = [g.get("name", "") for g in details.get("genres", []) or []]
    genre_lower = {g.lower() for g in genre_names}

    keyword_payload = details.get("keywords") or {}
    keywords = keyword_payload.get("keywords") or keyword_payload.get("results") or []
    keyword_names = {k.get("name", "").lower() for k in keywords if isinstance(k, dict)}

    if orig_lang == "ja" and ("animation" in genre_lower or "anime" in keyword_names):
        tags.add("Anime")

    try:
        if float(doc.get("rating") or details.get("vote_average") or 0) >= 7.5:
            tags.add("Top Rated")
    except Exception:
        pass

    year = doc.get("year") or doc.get("parsed_year")
    if year:
        try:
            if int(year) >= datetime.now().year - 1:
                tags.add("Recently Added")
        except Exception:
            pass

    for p_name in _extract_provider_names(watch_data):
        bucket = _provider_bucket(p_name)
        if bucket:
            providers.add(bucket)
            tags.add(bucket)

    return {
        "original_language": orig_lang,
        "origin_country": origin_country,
        "production_countries": production_countries,
        "watch_providers": sorted(providers),
        "auto_tags": sorted(tags),
    }


async def get_auto_catalog_settings(db) -> dict:
    state = await db.db["state"].find_one({"_id": "auto_catalog_settings"}) or {}
    configured = isinstance(state.get("enabled_keys"), list)
    enabled_keys = state.get("enabled_keys") if configured else []
    enabled_set = {k for k in enabled_keys if k in CATALOG_BY_KEY}

    definitions = []
    for item in AUTO_CATALOG_DEFINITIONS:
        definitions.append({
            **item,
            "enabled": item["key"] in enabled_set,
        })

    return {
        "configured": configured,
        "enabled_keys": sorted(enabled_set),
        "definitions": definitions,
        "region": AUTO_CATALOG_REGION,
    }


async def update_auto_catalog_settings(db, enabled_keys: List[str]) -> dict:
    clean_keys = sorted({str(k) for k in enabled_keys if str(k) in CATALOG_BY_KEY})
    now = datetime.now(timezone.utc).timestamp()
    await db.db["state"].update_one(
        {"_id": "auto_catalog_settings"},
        {"$set": {"enabled_keys": clean_keys, "updated_at": now}},
        upsert=True,
    )
    return await get_auto_catalog_settings(db)


async def get_auto_catalog_sync_status(db) -> dict:
    state = await db.db["state"].find_one({"_id": "auto_catalog_sync"}) or {}
    state.pop("_id", None)
    return state or {"running": False, "status": "idle", "scanned": 0, "classified": 0}


async def run_auto_catalog_sync(db, tmdb_api_key: Optional[str] = None, force_refresh: bool = False) -> dict:
    if _auto_sync_lock.locked():
        return {"running": True, "message": "Auto catalog sync is already running."}

    async with _auto_sync_lock:
        started_at = datetime.now(timezone.utc).timestamp()
        await db.db["state"].update_one(
            {"_id": "auto_catalog_sync"},
            {"$set": {
                "running": True,
                "message": "Auto catalog sync running...",
                "started_at": started_at,
                "finished_at": None,
                "scanned": 0,
                "classified": 0,
            }},
            upsert=True,
        )

        settings = await get_auto_catalog_settings(db)
        enabled_keys = set(settings.get("enabled_keys") or [])
        enabled_names = {CATALOG_BY_KEY[k]["name"] for k in enabled_keys if k in CATALOG_BY_KEY}

        if not enabled_names:
            summary = {
                "running": False,
                "message": "No auto catalogs enabled. Save selections first.",
                "scanned": 0,
                "classified": 0,
                "finished_at": datetime.now(timezone.utc).timestamp(),
            }
            await db.db["state"].update_one({"_id": "auto_catalog_sync"}, {"$set": summary}, upsert=True)
            return summary

        catalog_items: Dict[str, List[dict]] = {}
        scanned = 0
        classified = 0

        cursor = db.media.find({"tmdb_id": {"$exists": True, "$ne": None}})
        all_docs = await cursor.to_list(length=10000)
        scanned = len(all_docs)

        timeout = httpx.Timeout(15.0, connect=8.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            for doc in all_docs:
                details = {}
                watch_data = {}
                tmdb_id = doc.get("tmdb_id")
                media_type = "tv" if doc.get("media_type") in ["tv", "series", "anime"] else "movie"

                if tmdb_api_key and tmdb_id:
                    try:
                        det_resp = await client.get(
                            f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}",
                            params={"api_key": tmdb_api_key, "append_to_response": "keywords"},
                        )
                        if det_resp.status_code == 200:
                            details = det_resp.json()

                        watch_resp = await client.get(
                            f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/watch/providers",
                            params={"api_key": tmdb_api_key},
                        )
                        if watch_resp.status_code == 200:
                            watch_data = watch_resp.json()
                    except Exception as e:
                        logger.warning(f"TMDB query error for {tmdb_id}: {e}")

                classification = classify_media_from_tmdb(doc, details, watch_data, enabled_names)
                classified += 1

                item = _doc_item(doc)
                for tag in classification.get("auto_tags", []):
                    if tag in enabled_names:
                        catalog_items.setdefault(tag, []).append(item)

        # Rebuild custom_catalogs collection for auto entries
        now = datetime.now(timezone.utc).timestamp()
        for name, items in catalog_items.items():
            # Deduplicate items by tmdb_id + media_type
            seen = set()
            unique = []
            for it in items:
                k = (it["media_type"], it["tmdb_id"])
                if k not in seen:
                    seen.add(k)
                    unique.append(it)

            await db.custom_catalogs.update_one(
                {"auto_key": _catalog_key(name)},
                {
                    "$set": {
                        "name": name,
                        "visible": True,
                        "auto": True,
                        "auto_key": _catalog_key(name),
                        "items": unique,
                        "item_count": len(unique),
                        "updated_at": now,
                    },
                    "$setOnInsert": {
                        "created_at": now,
                        "visibility": "public",
                        "allowed_tokens": [],
                    },
                },
                upsert=True,
            )

        # Hide any auto catalogs that are disabled
        active_keys = {_catalog_key(name) for name in enabled_names}
        await db.custom_catalogs.update_many(
            {"auto": True, "auto_key": {"$nin": list(active_keys)}},
            {"$set": {"visible": False, "items": [], "item_count": 0, "updated_at": now}},
        )

        summary = {
            "running": False,
            "message": "Auto catalog sync complete.",
            "scanned": scanned,
            "classified": classified,
            "finished_at": datetime.now(timezone.utc).timestamp(),
        }
        await db.db["state"].update_one({"_id": "auto_catalog_sync"}, {"$set": summary}, upsert=True)
        return summary


def start_auto_catalog_sync_background(db, tmdb_api_key: Optional[str] = None, force_refresh: bool = False):
    global _auto_sync_task
    if _auto_sync_task and not _auto_sync_task.done():
        return {"running": True, "message": "Auto sync already in progress"}
    _auto_sync_task = asyncio.create_task(run_auto_catalog_sync(db, tmdb_api_key=tmdb_api_key, force_refresh=force_refresh))
    return {"running": True, "message": "Auto sync started in background"}
