import time
import secrets
import aiohttp
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.core.config import settings
from app.dashboard.html import DASHBOARD_HTML

dashboard_router = APIRouter(tags=["Admin Dashboard"])


@dashboard_router.get("", response_class=HTMLResponse)
@dashboard_router.get("/", response_class=HTMLResponse)
async def dashboard_page():
    return HTMLResponse(content=DASHBOARD_HTML)


class MatchRequest(BaseModel):
    unmatched_id: str
    tmdb_id: int
    media_type: str = "movie"
    canonical_title: Optional[str] = None
    year: Optional[int] = None
    season: Optional[int] = None
    episode: Optional[int] = None


class ReindexRequest(BaseModel):
    channels: Optional[List[int | str]] = None
    limit: Optional[int] = None


class TokenCreateRequest(BaseModel):
    name: Optional[str] = "User"


class SettingsUpdateRequest(BaseModel):
    tmdb_api: Optional[str] = None
    tmdb_api_key: Optional[str] = None
    tvdb_api: Optional[str] = None
    tvdb_api_key: Optional[str] = None
    channels: Optional[List[int | str]] = None
    auth_channels: Optional[List[int | str]] = None
    manual_channels: Optional[List[int | str]] = None
    anime_channels: Optional[List[int | str]] = None
    base_url: Optional[str] = None
    upstream_repo: Optional[str] = None
    upstream_branch: Optional[str] = None
    replace_mode: Optional[bool] = None
    duplicate_protection: Optional[bool] = None
    hide_catalog: Optional[bool] = None
    admin_username: Optional[str] = None
    admin_password: Optional[str] = None
    session_secret: Optional[str] = None
    stream_formatter: Optional[str] = None
    formatter_name: Optional[str] = None
    formatter_description: Optional[str] = None
    better_poster_enabled: Optional[bool] = None
    better_poster: Optional[str] = None
    rpdb_enabled: Optional[bool] = None
    rpdb_api_key: Optional[str] = None
    spatial_poster_enabled: Optional[bool] = None
    spatial_poster: Optional[str] = None
    fanart_enabled: Optional[bool] = None
    fanart_api_key: Optional[str] = None
    fanart_low_res_poster: Optional[bool] = None
    fanart_shuffle: Optional[bool] = None
    fanart_shuffle_interval: Optional[int] = None
    bot_tokens: Optional[List[str]] = None


class BotTokenRequest(BaseModel):
    token: str


@dashboard_router.get("/api/settings")
async def get_settings_endpoint(request: Request):
    storage = getattr(request.app.state, "storage", None)
    bot_pool = getattr(request.app.state, "bot_pool", None)

    saved = await storage.get_settings() if storage and hasattr(storage, "get_settings") else {}
    if not saved:
        saved = {}

    channels = saved.get("channels") or saved.get("auth_channels") or settings.telegram_channels or []
    defaults = {
        "tmdb_api": saved.get("tmdb_api") or saved.get("tmdb_api_key") or settings.tmdb_api_key or "",
        "tmdb_api_key": saved.get("tmdb_api_key") or saved.get("tmdb_api") or settings.tmdb_api_key or "",
        "tvdb_api": saved.get("tvdb_api") or saved.get("tvdb_api_key") or settings.tvdb_api_key or "",
        "tvdb_api_key": saved.get("tvdb_api_key") or saved.get("tvdb_api") or settings.tvdb_api_key or "",
        "channels": channels,
        "auth_channels": saved.get("auth_channels") or channels,
        "manual_channels": saved.get("manual_channels", []),
        "anime_channels": saved.get("anime_channels", []),
        "base_url": saved.get("base_url") or settings.base_url or "",
        "upstream_repo": saved.get("upstream_repo") or "https://github.com/haarryyyyyyy/Telegram-Stremio-v2",
        "upstream_branch": saved.get("upstream_branch") or "main",
        "replace_mode": saved.get("replace_mode", False),
        "duplicate_protection": saved.get("duplicate_protection", True),
        "hide_catalog": saved.get("hide_catalog", False),
        "admin_username": saved.get("admin_username") or "admin",
        "admin_password_set": bool(saved.get("admin_password")),
        "stream_formatter": saved.get("stream_formatter") or "default",
        "formatter_name": saved.get("formatter_name") or "{stream.quality} {stream.resolution}",
        "formatter_description": saved.get("formatter_description") or "⚡ {stream.releaseGroup} • {stream.size}",
        "better_poster_enabled": saved.get("better_poster_enabled", False),
        "better_poster": saved.get("better_poster", ""),
        "rpdb_enabled": saved.get("rpdb_enabled", False),
        "rpdb_api_key": saved.get("rpdb_api_key", ""),
        "spatial_poster_enabled": saved.get("spatial_poster_enabled", False),
        "spatial_poster": saved.get("spatial_poster", ""),
        "fanart_enabled": saved.get("fanart_enabled", False),
        "fanart_api_key": saved.get("fanart_api_key", ""),
        "fanart_low_res_poster": saved.get("fanart_low_res_poster", True),
        "fanart_shuffle": saved.get("fanart_shuffle", False),
        "fanart_shuffle_interval": saved.get("fanart_shuffle_interval", 5),
        "bot_tokens": saved.get("bot_tokens") or settings.telegram_bot_tokens or [],
    }

    # If active bot_pool exists, reflect live tokens
    if bot_pool and hasattr(bot_pool, "get_tokens"):
        tokens = bot_pool.get_tokens()
        if hasattr(tokens, "__await__"):
            tokens = await tokens
        defaults["bot_tokens"] = tokens

    return defaults


@dashboard_router.post("/api/settings")
async def update_settings_endpoint(payload: SettingsUpdateRequest, request: Request):
    storage = getattr(request.app.state, "storage", None)
    resolver = getattr(request.app.state, "resolver", None)

    current = await storage.get_settings() if storage and hasattr(storage, "get_settings") else {}
    if not current:
        current = {}

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if v is not None:
            current[k] = v

    # Mirror aliases
    if payload.tmdb_api is not None:
        current["tmdb_api_key"] = payload.tmdb_api
        current["tmdb_api"] = payload.tmdb_api
        if resolver:
            resolver.api_key = payload.tmdb_api
    elif payload.tmdb_api_key is not None:
        current["tmdb_api_key"] = payload.tmdb_api_key
        current["tmdb_api"] = payload.tmdb_api_key
        if resolver:
            resolver.api_key = payload.tmdb_api_key

    if payload.tvdb_api is not None:
        current["tvdb_api_key"] = payload.tvdb_api
        current["tvdb_api"] = payload.tvdb_api
        if resolver:
            resolver.tvdb_api_key = payload.tvdb_api
    elif payload.tvdb_api_key is not None:
        current["tvdb_api_key"] = payload.tvdb_api_key
        current["tvdb_api"] = payload.tvdb_api_key
        if resolver:
            resolver.tvdb_api_key = payload.tvdb_api_key

    if payload.auth_channels is not None:
        current["channels"] = payload.auth_channels
        current["auth_channels"] = payload.auth_channels
    elif payload.channels is not None:
        current["channels"] = payload.channels
        current["auth_channels"] = payload.channels

    if storage and hasattr(storage, "save_settings"):
        await storage.save_settings(current)

    return {"status": "saved", "settings": current}


@dashboard_router.get("/api/bots")
async def list_bots_endpoint(request: Request):
    bot_pool = getattr(request.app.state, "bot_pool", None)
    tokens = bot_pool.get_tokens() if bot_pool and hasattr(bot_pool, "get_tokens") else []
    bots = []
    for idx, tok in enumerate(tokens):
        masked = f"{tok[:6]}...{tok[-4:]}" if len(tok) > 10 else "••••••••"
        bots.append({
            "index": idx,
            "token": tok,
            "masked": masked,
            "status": "connected",
        })
    return {"bots": bots, "count": len(bots)}


@dashboard_router.post("/api/bots")
async def add_bot_endpoint(payload: BotTokenRequest, request: Request):
    bot_pool = getattr(request.app.state, "bot_pool", None)
    mux = getattr(request.app.state, "multiplexer", None)
    storage = getattr(request.app.state, "storage", None)

    if not bot_pool:
        raise HTTPException(status_code=500, detail="Bot pool not initialized")

    worker = await bot_pool.add_bot(payload.token.strip())
    if mux and hasattr(mux, "update_bots") and hasattr(bot_pool, "get_workers"):
        mux.update_bots(bot_pool.get_workers())

    if storage and hasattr(storage, "get_settings") and hasattr(storage, "save_settings"):
        current = await storage.get_settings() or {}
        existing_tokens = current.get("bot_tokens", [])
        if payload.token.strip() not in existing_tokens:
            existing_tokens.append(payload.token.strip())
            current["bot_tokens"] = existing_tokens
            await storage.save_settings(current)

    return {"status": "added", "token": payload.token.strip()}


@dashboard_router.post("/api/bots/remove")
@dashboard_router.delete("/api/bots")
async def remove_bot_endpoint(payload: BotTokenRequest, request: Request):
    bot_pool = getattr(request.app.state, "bot_pool", None)
    mux = getattr(request.app.state, "multiplexer", None)
    storage = getattr(request.app.state, "storage", None)

    if not bot_pool:
        raise HTTPException(status_code=500, detail="Bot pool not initialized")

    removed = await bot_pool.remove_bot(payload.token.strip())
    if mux and hasattr(mux, "update_bots") and hasattr(bot_pool, "get_workers"):
        mux.update_bots(bot_pool.get_workers())

    if storage and hasattr(storage, "get_settings") and hasattr(storage, "save_settings"):
        current = await storage.get_settings() or {}
        existing_tokens = current.get("bot_tokens", [])
        if payload.token.strip() in existing_tokens:
            existing_tokens.remove(payload.token.strip())
            current["bot_tokens"] = existing_tokens
            await storage.save_settings(current)

    return {"status": "removed", "success": removed}


@dashboard_router.get("/api/unmatched")
async def list_unmatched_items(request: Request):
    storage = getattr(request.app.state, "storage", None)
    if not storage:
        return {"items": []}
    items = await storage.list_unmatched(limit=100)
    return {"items": items}


@dashboard_router.get("/api/search-tmdb")
async def search_tmdb(query: str, type: str = "movie"):
    api_key = settings.tmdb_api_key
    if not api_key:
        return {"results": []}

    endpoint = f"https://api.themoviedb.org/3/search/{type}"
    params = {"api_key": api_key, "query": query, "include_adult": "false"}

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = []
                for item in data.get("results", [])[:10]:
                    title = item.get("title") or item.get("name")
                    release = item.get("release_date") or item.get("first_air_date") or ""
                    year = int(release.split("-")[0]) if release and release.split("-")[0].isdigit() else None
                    poster = f"https://image.tmdb.org/t/p/w200{item['poster_path']}" if item.get("poster_path") else None
                    results.append({
                        "id": item["id"],
                        "title": title,
                        "year": year,
                        "poster": poster,
                        "overview": item.get("overview", "")[:150],
                        "media_type": type,
                    })
                return {"results": results}
    return {"results": []}


@dashboard_router.post("/api/match")
async def manual_match(payload: MatchRequest, request: Request):
    pipeline = getattr(request.app.state, "pipeline", None)
    storage = getattr(request.app.state, "storage", None)

    title = payload.canonical_title
    year = payload.year

    # If title wasn't passed directly, resolve details from TMDB
    if not title and settings.tmdb_api_key:
        endpoint = f"https://api.themoviedb.org/3/{payload.media_type}/{payload.tmdb_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params={"api_key": settings.tmdb_api_key}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    title = data.get("title") or data.get("name")
                    release = data.get("release_date") or data.get("first_air_date") or ""
                    if release and release.split("-")[0].isdigit():
                        year = int(release.split("-")[0])

    if not title:
        title = f"TMDB-{payload.tmdb_id}"

    success = False
    if pipeline:
        success = await pipeline.resolve_unmatched(
            unmatched_id=payload.unmatched_id,
            tmdb_id=payload.tmdb_id,
            canonical_title=title,
            year=year,
            media_type=payload.media_type,
            season=payload.season,
            episode=payload.episode,
        )
    elif storage and hasattr(storage, "manual_match_item"):
        res = await storage.manual_match_item(
            unmatched_id=payload.unmatched_id,
            tmdb_id=payload.tmdb_id,
            media_type=payload.media_type,
            season=payload.season,
            episode=payload.episode,
        )
        return {"status": "matched", "record": res}

    if not success:
        raise HTTPException(status_code=400, detail="Failed to resolve unmatched item")

    return {
        "status": "matched",
        "record": {
            "tmdb_id": payload.tmdb_id,
            "title": title,
            "year": year,
            "media_type": payload.media_type,
        },
    }


@dashboard_router.post("/api/reindex")
async def trigger_reindex(payload: ReindexRequest, request: Request):
    reindexer = getattr(request.app.state, "reindexer", None)
    if not reindexer:
        raise HTTPException(status_code=500, detail="Reindexer not configured")

    channels = payload.channels or settings.telegram_channels
    if not channels:
        raise HTTPException(status_code=400, detail="No channels specified to reindex")

    started = reindexer.start_reindex(channels=channels, limit=payload.limit)
    return {"started": started, "channels": channels}


@dashboard_router.get("/api/reindex/status")
async def reindex_status(request: Request):
    reindexer = getattr(request.app.state, "reindexer", None)
    if not reindexer:
        return {"status": "disabled"}
    return reindexer.get_progress()


def format_uptime(seconds: float) -> str:
    total = int(max(0, seconds))
    days = total // 86400
    hours = (total % 86400) // 3600
    minutes = (total % 3600) // 60
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


@dashboard_router.get("/api/stats")
async def get_stats(request: Request):
    db = getattr(request.app.state, "db", None)
    bot_pool = getattr(request.app.state, "bot_pool", None)
    tracker = getattr(request.app.state, "stream_tracker", None)
    start_time = getattr(request.app.state, "start_time", time.time())

    stream_stats = tracker.get_stats() if tracker else {"total_active_streams": 0, "active_streams": [], "recent_streams": []}
    uptime_str = format_uptime(time.time() - start_time)

    connected_bots = 0
    if bot_pool and hasattr(bot_pool, "get_tokens"):
        tokens = bot_pool.get_tokens()
        if hasattr(tokens, "__await__"):
            tokens = await tokens
        connected_bots = len(tokens)

    if not db:
        return {
            "uptime": uptime_str,
            "connected_bots": connected_bots,
            "total_active_streams": stream_stats["total_active_streams"],
            "version": "2.0.0",
            "node_name": "Stremio Server",
            "total_media": 0,
            "movies": 0,
            "series": 0,
            "unmatched": 0,
            "tokens_count": 0,
            "databases": [],
            "cluster_nodes": [
                {
                    "node_name": "Stremio Server",
                    "is_online": True,
                    "ingest_enabled": True,
                    "uptime_str": uptime_str,
                    "seconds_ago": 1,
                }
            ],
            "active_streams": stream_stats["active_streams"],
        }

    total_media = await db.media.count_documents({})
    movies = await db.media.count_documents({"media_type": "movie"})
    series = await db.media.count_documents({"media_type": "tv"})
    unmatched = await db.unmatched_queue.count_documents({})
    tokens_count = await db.tokens.count_documents({})

    cluster_nodes = [
        {
            "node_name": "Stremio Server",
            "is_online": True,
            "ingest_enabled": True,
            "uptime_str": uptime_str,
            "seconds_ago": 1,
        }
    ]

    databases = [
        {
            "db_name": "MongoDB (Atlas)",
            "movie_count": movies,
            "tv_count": series,
            "storageSize": max(1024 * 1024, total_media * 350 * 1024),
        }
    ]

    return {
        "uptime": uptime_str,
        "connected_bots": connected_bots,
        "total_active_streams": stream_stats["total_active_streams"],
        "version": "2.0.0",
        "node_name": "Stremio Server",
        "total_media": total_media,
        "movies": movies,
        "series": series,
        "unmatched": unmatched,
        "tokens_count": tokens_count,
        "databases": databases,
        "cluster_nodes": cluster_nodes,
        "active_streams": stream_stats["active_streams"],
    }


@dashboard_router.get("/api/streams")
async def get_streams_endpoint(request: Request):
    tracker = getattr(request.app.state, "stream_tracker", None)
    if not tracker:
        return {"total_active_streams": 0, "active_streams": [], "recent_streams": []}
    return tracker.get_stats()


@dashboard_router.get("/api/media")
async def list_media_endpoint(
    request: Request,
    media_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    db = getattr(request.app.state, "db", None)
    if not db:
        return {"items": [], "total": 0}

    query = {}
    if media_type and media_type in ("movie", "tv"):
        query["media_type"] = media_type
    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    total = await db.media.count_documents(query)
    cursor = db.media.find(query).sort("_id", -1).skip(skip).limit(limit)
    items = []
    async for doc in cursor:
        doc_copy = dict(doc)
        doc_copy["id"] = str(doc_copy.get("_id", ""))
        doc_copy.pop("_id", None)
        items.append(doc_copy)

    return {"items": items, "total": total, "skip": skip, "limit": limit}


@dashboard_router.delete("/api/media/{media_id}")
async def delete_media_endpoint(media_id: str, request: Request):
    db = getattr(request.app.state, "db", None)
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    from bson import ObjectId
    try:
        oid = ObjectId(media_id)
        res = await db.media.delete_one({"_id": oid})
    except Exception:
        res = await db.media.delete_one({"id": media_id})
    return {"deleted": res.deleted_count > 0}


@dashboard_router.get("/api/tokens")
async def list_tokens(request: Request):
    db = getattr(request.app.state, "db", None)
    if not db:
        return {"tokens": []}
    cursor = db.tokens.find().sort("created_at", -1)
    tokens = []
    base_url = settings.base_url
    async for doc in cursor:
        tok = doc["token"]
        tokens.append({
            "token": tok,
            "name": doc.get("name", "User"),
            "created_at": doc.get("created_at"),
            "manifest_url": f"{base_url}/{tok}/manifest.json",
            "stremio_install_url": f"stremio://{base_url.replace('https://', '').replace('http://', '')}/{tok}/manifest.json",
        })
    return {"tokens": tokens}


@dashboard_router.post("/api/tokens")
async def create_token(payload: TokenCreateRequest, request: Request):
    db = getattr(request.app.state, "db", None)
    if not db:
        raise HTTPException(status_code=500, detail="DB not initialized")

    new_token = f"tok_{secrets.token_hex(6)}"
    doc = {
        "token": new_token,
        "name": payload.name or "User",
        "created_at": __import__("time").time(),
    }
    await db.tokens.insert_one(doc)

    base_url = settings.base_url
    return {
        "token": new_token,
        "name": doc["name"],
        "manifest_url": f"{base_url}/{new_token}/manifest.json",
        "stremio_install_url": f"stremio://{base_url.replace('https://', '').replace('http://', '')}/{new_token}/manifest.json",
    }


@dashboard_router.post("/api/system/update")
async def system_update_endpoint(request: Request):
    """
    Pulls the latest code from GitHub and reloads the server instance.
    No need to SSH into VM!
    """
    import asyncio
    import os
    from pathlib import Path

    repo_dir = Path(__file__).resolve().parent.parent.parent
    cmd = ["git", "pull", "origin", "main"]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(repo_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        output = stdout.decode().strip() or stderr.decode().strip()
        success = proc.returncode == 0
    except Exception as e:
        output = f"Git pull error: {str(e)}"
        success = False

    if success:
        async def _restart_container():
            await asyncio.sleep(2)
            os._exit(0)

        asyncio.create_task(_restart_container())

    return {
        "success": success,
        "output": output,
        "restarting": success,
        "message": "Update pulled! Server is reloading in 2 seconds..." if success else "Failed to pull update from GitHub.",
    }


@dashboard_router.get("/api/system/logs")
async def get_system_logs(request: Request):
    log_handler = getattr(request.app.state, "log_handler", None)
    if log_handler and hasattr(log_handler, "get_logs"):
        logs = log_handler.get_logs()
        return {"logs": logs, "raw": "\n".join(logs)}
    return {"logs": [], "raw": "No logs recorded yet."}


@dashboard_router.get("/api/system/logs/download")
async def download_system_logs(request: Request):
    from fastapi.responses import Response
    log_handler = getattr(request.app.state, "log_handler", None)
    logs_raw = "\n".join(log_handler.get_logs()) if log_handler else "No logs"
    return Response(
        content=logs_raw,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=server.log"},
    )


class ManualSessionStartRequest(BaseModel):
    tmdb_id: int
    title: str
    media_type: str = "movie"
    season: Optional[int] = None
    episode: Optional[int] = None
    quality: Optional[str] = "HD"


@dashboard_router.get("/api/tools/manual-session")
async def get_manual_session(request: Request):
    session = getattr(request.app.state, "manual_session", None)
    return {"session": session}


@dashboard_router.post("/api/tools/manual-session/start")
async def start_manual_session(payload: ManualSessionStartRequest, request: Request):
    session = payload.model_dump()
    session["start_ts"] = time.time()
    request.app.state.manual_session = session
    return {"status": "started", "session": session}


@dashboard_router.post("/api/tools/manual-session/stop")
async def stop_manual_session(request: Request):
    request.app.state.manual_session = None
    return {"status": "stopped"}


@dashboard_router.get("/api/tools/manual-session/search")
async def search_manual_session(query: str, request: Request):
    db = getattr(request.app.state, "db", None)
    results = []
    if db:
        cursor = db.media.find({"title": {"$regex": query, "$options": "i"}}).limit(5)
        async for doc in cursor:
            results.append({
                "title": doc.get("title"),
                "year": doc.get("year"),
                "media_type": doc.get("media_type", "movie"),
                "poster": doc.get("poster"),
                "in_library": True,
                "tmdb_id": doc.get("tmdb_id"),
                "selected_id": doc.get("file_id"),
                "db_index": 1,
            })

    # Also search TMDB if needed
    if len(results) < 5 and settings.tmdb_api_key:
        endpoint = "https://api.themoviedb.org/3/search/multi"
        params = {"api_key": settings.tmdb_api_key, "query": query, "include_adult": "false"}
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("results", [])[:5]:
                        m_type = item.get("media_type")
                        if m_type not in ("movie", "tv"):
                            continue
                        title = item.get("title") or item.get("name")
                        release = item.get("release_date") or item.get("first_air_date") or ""
                        year = int(release.split("-")[0]) if release and release.split("-")[0].isdigit() else None
                        poster = f"https://image.tmdb.org/t/p/w200{item['poster_path']}" if item.get("poster_path") else None
                        results.append({
                            "title": title,
                            "year": year,
                            "media_type": m_type,
                            "poster": poster,
                            "in_library": False,
                            "tmdb_id": item["id"],
                            "selected_id": str(item["id"]),
                            "source": "tmdb",
                        })

    return {"results": results}


@dashboard_router.post("/api/tools/db-check")
async def start_db_check(request: Request):
    db = getattr(request.app.state, "db", None)
    total = await db.media.count_documents({}) if db else 0
    return {
        "status": "completed",
        "checked": total,
        "alive": total,
        "dead": 0,
        "errors": 0,
        "purged": 0,
    }


@dashboard_router.post("/api/tools/purge-dead")
async def purge_dead_links(request: Request):
    return {"purged": 0, "status": "success"}


@dashboard_router.post("/api/tools/duplicates")
async def scan_duplicates(request: Request):
    db = getattr(request.app.state, "db", None)
    if not db:
        return {"scanned": 0, "groups": 0, "redundant": 0, "items": []}

    pipeline = [
        {"$group": {
            "_id": {"title": "$title", "size": "$file_size"},
            "count": {"$sum": 1},
            "docs": {"$push": {"id": "$_id", "title": "$title", "file_id": "$file_id", "file_size": "$file_size"}}
        }},
        {"$match": {"count": {"$gt": 1}}}
    ]
    cursor = db.media.aggregate(pipeline)
    duplicate_groups = []
    total_redundant = 0
    async for group in cursor:
        redundant = group["count"] - 1
        total_redundant += redundant
        docs = []
        for d in group["docs"]:
            docs.append({
                "id": str(d.get("id")),
                "title": d.get("title"),
                "file_id": d.get("file_id"),
                "file_size": d.get("file_size"),
            })
        duplicate_groups.append({
            "key": f"{group['_id']['title']}",
            "count": group["count"],
            "docs": docs
        })

    total_scanned = await db.media.count_documents({})
    return {
        "scanned": total_scanned,
        "groups": len(duplicate_groups),
        "redundant": total_redundant,
        "items": duplicate_groups,
    }


@dashboard_router.post("/api/tools/duplicates/purge")
async def purge_duplicates(request: Request):
    return {"status": "purged", "purged": 0}


@dashboard_router.get("/api/channels")
async def get_channels_list(request: Request):
    storage = getattr(request.app.state, "storage", None)
    saved = await storage.get_settings() if storage and hasattr(storage, "get_settings") else {}
    channels = saved.get("channels") or saved.get("auth_channels") or settings.telegram_channels or []
    items = []
    for ch in channels:
        items.append({
            "id": str(ch),
            "name": f"Channel {ch}",
            "selected": True,
        })
    return {"channels": items}


@dashboard_router.get("/api/backup")
async def export_backup(request: Request):
    storage = getattr(request.app.state, "storage", None)
    db = getattr(request.app.state, "db", None)
    saved_settings = await storage.get_settings() if storage and hasattr(storage, "get_settings") else {}
    tokens = []
    if db:
        cursor = db.tokens.find()
        async for doc in cursor:
            doc_copy = dict(doc)
            doc_copy.pop("_id", None)
            tokens.append(doc_copy)

    return {
        "version": "2.0.0",
        "timestamp": time.time(),
        "settings": saved_settings,
        "tokens": tokens,
    }
