import secrets
from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, Request, HTTPException, Header, Response
from fastapi.responses import JSONResponse, StreamingResponse
from app.core.config import settings
from app.stremio.catalog import CatalogManager, StremioMetaItem

stremio_router = APIRouter(tags=["Stremio"])


@stremio_router.get("/{token}/manifest.json")
async def get_manifest(token: str, request: Request):
    catalogs = [
        {
            "id": "spotlight",
            "type": "movie",
            "name": "🌟 15m Spotlight",
            "extra": [
                {"name": "search", "isRequired": False},
                {"name": "skip", "isRequired": False},
            ],
        },
        {
            "id": "recent",
            "type": "movie",
            "name": "🆕 Recently Added",
            "extra": [
                {"name": "search", "isRequired": False},
                {"name": "skip", "isRequired": False},
            ],
        },
        {
            "id": "recommended",
            "type": "movie",
            "name": "🎬 Recommended For You",
            "extra": [
                {"name": "search", "isRequired": False},
                {"name": "skip", "isRequired": False},
            ],
        },
        {
            "id": "spotlight",
            "type": "series",
            "name": "🌟 15m TV & Anime",
            "extra": [
                {"name": "search", "isRequired": False},
                {"name": "skip", "isRequired": False},
            ],
        },
        {
            "id": "recent",
            "type": "series",
            "name": "🆕 Recent TV & Anime",
            "extra": [
                {"name": "search", "isRequired": False},
                {"name": "skip", "isRequired": False},
            ],
        },
    ]

    db = getattr(request.app.state, "db", None)
    if db:
        try:
            custom_catalogs = await db.get_custom_catalogs(visible_only=True)
            for c in custom_catalogs:
                # Visibility check: public or matching token
                vis = c.get("visibility", "public")
                if vis == "owner":
                    continue
                if vis == "tokens" and token not in (c.get("allowed_tokens") or []):
                    continue

                cid = f"custom_{c['_id']}"
                items = c.get("items") or []
                has_movie = any(it.get("media_type") == "movie" for it in items)
                has_series = any(it.get("media_type") in ("tv", "series") for it in items)
                cat_name = c.get("name") or "Catalog"

                if has_movie or not items:
                    catalogs.append({
                        "id": cid,
                        "type": "movie",
                        "name": cat_name,
                        "extra": [
                            {"name": "search", "isRequired": False},
                            {"name": "skip", "isRequired": False},
                        ],
                    })
                if has_series:
                    catalogs.append({
                        "id": cid,
                        "type": "series",
                        "name": cat_name,
                        "extra": [
                            {"name": "search", "isRequired": False},
                            {"name": "skip", "isRequired": False},
                        ],
                    })

            # Apply order
            order = await db.get_catalog_order()
            if order:
                rank = {k: i for i, k in enumerate(order)}

                def _crank(cat_entry):
                    k = f"{cat_entry.get('id')}::{cat_entry.get('type')}"
                    return rank.get(k, rank.get(cat_entry.get("id"), len(order) + 1))

                catalogs.sort(key=_crank)
        except Exception:
            pass

    return {
        "id": "community.telegram.stremio.v2",
        "version": "2.0.0",
        "name": "Telegram Stremio V2",
        "description": "Blazing-fast multi-bot Telegram streaming engine with dynamic 15m spotlight and smart catalogs.",
        "resources": ["catalog", "stream"],
        "types": ["movie", "series"],
        "catalogs": catalogs,
    }


@stremio_router.get("/{token}/catalog/{type}/{id}/search={query}.json")
async def get_catalog_search_path_handler(
    token: str,
    type: str,
    id: str,
    query: str,
    request: Request,
):
    catalog_mgr: CatalogManager = request.app.state.catalog_manager
    metas = await catalog_mgr.search_catalog(catalog_type=type, query=query)
    return {
        "metas": [
            {
                "id": m.id,
                "type": m.type,
                "name": m.name,
                "poster": m.poster,
                "year": m.year,
            }
            for m in metas
        ]
    }


@stremio_router.get("/{token}/catalog/{type}/{id}.json")
async def get_catalog_handler(
    token: str,
    type: str,
    id: str,
    request: Request,
    skip: int = 0,
    search: Optional[str] = None,
):
    catalog_mgr: CatalogManager = request.app.state.catalog_manager
    if search:
        metas = await catalog_mgr.search_catalog(catalog_type=type, query=search)
    else:
        metas = await catalog_mgr.get_catalog(
            token=token,
            catalog_type=type,
            catalog_id=id,
            skip=skip,
        )
    return {
        "metas": [
            {
                "id": m.id,
                "type": m.type,
                "name": m.name,
                "poster": m.poster,
                "year": m.year,
            }
            for m in metas
        ]
    }


@stremio_router.get("/{token}/stream/{type}/{id}.json")
async def get_stream_handler(
    token: str,
    type: str,
    id: str,
    request: Request,
):
    db = request.app.state.db
    # id format: tmdb:19169 or tmdb:19169:1:10 (for series)
    parts = id.split(":")
    if len(parts) < 2 or parts[0] != "tmdb":
        return {"streams": []}

    try:
        tmdb_id = int(parts[1])
    except ValueError:
        return {"streams": []}

    query = {"tmdb_id": tmdb_id}
    if len(parts) >= 4:
        # season:episode
        query["season"] = int(parts[2])
        query["episode"] = int(parts[3])

    cursor = db.media.find(query)
    streams = []
    base_url = settings.base_url

    async for doc in cursor:
        quality_label = doc.get("quality") or "HD"
        size_gb = round(doc.get("file_size", 0) / (1024 ** 3), 1)
        size_str = f" • {size_gb} GB" if size_gb > 0 else ""
        alias_str = f" [{doc['matched_alias']}]" if doc.get("matched_alias") and doc["matched_alias"] != doc["title"] else ""

        title = f"⚡ [{quality_label}]{alias_str}{size_str}"
        file_id = doc.get("file_id", "")
        safe_filename = quote(f"{doc['title']}_{quality_label}.mkv")
        stream_url = f"{base_url}/{token}/dl/{file_id}/{safe_filename}"

        streams.append({
            "name": f"Telegram V2 ({quality_label})",
            "title": title,
            "url": stream_url,
        })

    return {"streams": streams}


@stremio_router.get("/{token}/dl/{file_id}/{filename}")
@stremio_router.head("/{token}/dl/{file_id}/{filename}")
async def stream_video_file(
    token: str,
    file_id: str,
    filename: str,
    request: Request,
    range: Optional[str] = Header(None),
):
    mux = getattr(request.app.state, "multiplexer", None)
    db = request.app.state.db

    # Look up file record for total size
    record = await db.media.find_one({"file_id": file_id})
    file_size = record.get("file_size", 0) if record else 0

    if file_size <= 0:
        raise HTTPException(status_code=404, detail="File metadata not found")

    # Parse HTTP Range header
    start = 0
    end = file_size - 1
    if range and range.startswith("bytes="):
        range_val = range.replace("bytes=", "").strip()
        parts = range_val.split("-")
        if parts[0]:
            start = int(parts[0])
        if len(parts) > 1 and parts[1]:
            end = int(parts[1])

    if start > end or end >= file_size:
        raise HTTPException(
            status_code=416,
            detail="Range Not Satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    content_length = end - start + 1
    headers = {
        "Content-Type": "video/x-matroska",
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Content-Length": str(content_length),
        "Accept-Ranges": "bytes",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=3600",
    }

    if request.method == "HEAD":
        return Response(status_code=206, headers=headers)

    tracker = getattr(request.app.state, "stream_tracker", None)
    stream_id = f"st_{secrets.token_hex(4)}"
    client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "127.0.0.1")
    user_title = record.get("title") if record else filename

    if tracker:
        tracker.start_stream(
            stream_id=stream_id,
            file_id=file_id,
            title=user_title,
            file_name=filename,
            file_size=file_size,
            ip=client_ip,
        )

    # Use multi-bot chunk multiplexer
    chunk_stream = mux.stream_range(file_id=file_id, start=start, end=end)

    async def _tracked_stream():
        try:
            async for chunk in chunk_stream:
                if tracker:
                    tracker.update_bytes(stream_id, len(chunk))
                yield chunk
            if tracker:
                tracker.finish_stream(stream_id, status="completed")
        except Exception:
            if tracker:
                tracker.finish_stream(stream_id, status="cancelled")
            raise

    return StreamingResponse(_tracked_stream(), status_code=206, headers=headers)
