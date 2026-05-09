import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from core.session.models import Session, Message

SESSION_DIR = Path("data/sessions")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

_LOCK = threading.Lock()
SESSION_TTL_HOURS = 24

# Persistence Layer - Handles where and how sessions are stored. 
# What it does?
#   a) Saves sessions to disk (data/sessions/)
#   b) Loads sessions by session_id
#   c) Serializes/deserializes session objects
# Design choice -
#   a) File-based JSON (simple, transparent, debuggable) 
#   b) Easily replaceable with - Redis, SQLite, PostgreSQL
# Why it matters?
# Without persistence -
#   a) Sessions die on restart
#   b) “Memory” is fake
#
class SessionStore: # Handles storage (in-memory for now, disk later)

    @staticmethod
    def save(session: Session):
        with _LOCK:
            session.last_accessed_at = datetime.utcnow().isoformat()
            path = SESSION_DIR / f"{session.session_id}.json"
            with open(path, "w") as f:
                json.dump(session.__dict__, f, default=lambda o: o.__dict__, indent=2)

    @staticmethod
    def load(session_id: str) -> Session | None:
        path = SESSION_DIR / f"{session_id}.json"
        if not path.exists():
            return None

        with _LOCK, open(path) as f:
            data = json.load(f)

        session = Session(
            session_id=data["session_id"],
            user_id=data["user_id"],
            summary=data.get("summary", ""),
            memory_vector_ids=data.get("memory_vector_ids", []),
            created_at=data.get("created_at", ""),
            last_accessed_at=data.get("last_accessed_at", "")
        )

        session.recent_messages = [
            Message(**m) for m in data.get("recent_messages", [])
        ]
        return session

    @staticmethod
    def cleanup_expired():
        now = datetime.utcnow()
        for file in SESSION_DIR.glob("*.json"):
            with open(file) as f:
                data = json.load(f)

            last_access = datetime.fromisoformat(data["last_accessed_at"])
            if now - last_access > timedelta(hours=SESSION_TTL_HOURS):
                file.unlink()