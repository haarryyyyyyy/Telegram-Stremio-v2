import time
from collections import deque
from typing import Dict, Any, List, Optional


class StreamTracker:
    def __init__(self, max_recent: int = 25):
        self.active_streams: Dict[str, Dict[str, Any]] = {}
        self.recent_streams: deque = deque(maxlen=max_recent)

    def start_stream(
        self,
        stream_id: str,
        file_id: str,
        title: str,
        file_name: str,
        file_size: int,
        client_index: int = 0,
        dc_id: Optional[int] = None,
        node_name: str = "Stremio Server",
        user_name: Optional[str] = None,
        ip: Optional[str] = None,
    ) -> Dict[str, Any]:
        session = {
            "stream_id": stream_id,
            "file_id": file_id,
            "title": title or file_name or "Unknown Video",
            "file_name": file_name,
            "file_size": file_size,
            "total_bytes": 0,
            "avg_mbps": 0.0,
            "start_ts": time.time(),
            "last_active_ts": time.time(),
            "status": "active",
            "client_index": client_index,
            "dc_id": dc_id or 4,
            "node_name": node_name,
            "user_name": user_name or ip or "Stremio Player",
            "ip": ip or "127.0.0.1",
        }
        self.active_streams[stream_id] = session
        return session

    def update_bytes(self, stream_id: str, byte_count: int):
        session = self.active_streams.get(stream_id)
        if not session:
            return
        session["total_bytes"] += byte_count
        now = time.time()
        session["last_active_ts"] = now
        elapsed = max(0.001, now - session["start_ts"])
        # avg_mbps = (bytes / (1024*1024)) / seconds
        session["avg_mbps"] = round((session["total_bytes"] / (1024 * 1024)) / elapsed, 3)

    def finish_stream(self, stream_id: str, status: str = "completed"):
        session = self.active_streams.pop(stream_id, None)
        if session:
            session["status"] = status
            session["end_ts"] = time.time()
            self.recent_streams.appendleft(session)

    def get_stats(self) -> Dict[str, Any]:
        # Clean up stale active streams that haven't sent chunks in >60 seconds
        now = time.time()
        stale_ids = [
            sid for sid, s in self.active_streams.items()
            if now - s.get("last_active_ts", s["start_ts"]) > 60
        ]
        for sid in stale_ids:
            self.finish_stream(sid, status="completed")

        active_list = list(self.active_streams.values())
        return {
            "total_active_streams": len(active_list),
            "active_streams": active_list,
            "recent_streams": list(self.recent_streams),
        }
