import json
from pathlib import Path
from core.session.models import Session

SESSION_DIR = Path("data/sessions")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

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
        path = SESSION_DIR / f"{session.session_id}.json"
        with open(path, "w") as f:
            json.dump(session.__dict__, f, default=lambda o: o.__dict__, indent=2)

    @staticmethod
    def load(session_id: str) -> Session | None:
        path = SESSION_DIR / f"{session_id}.json"
        if not path.exists():
            return None

        with open(path) as f:
            data = json.load(f)

        session = Session(
            session_id=data["session_id"],
            summary=data.get("summary", ""),
            memory_vector_ids=data.get("memory_vector_ids", []),
            created_at=data.get("created_at", "")
        )

        session.recent_messages = [
            Message(**m) for m in data.get("recent_messages", [])
        ]
        return session