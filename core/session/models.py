from dataclasses import dataclass, field
from typing import List
from datetime import datetime

# Session Data Blueprint - Defines the structure of a conversation session.
@dataclass
class Message:
    role: str        # "user" | "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat()) # auditing + summarization triggers

@dataclass
class Session:
    session_id: str # unique identity
    user_id: str    # enables per-user isolation
    recent_messages: List[Message] = field(default_factory=list)   # sliding window
    summary: str = ""           # compressed past
    memory_vector_ids: List[str] = field(default_factory=list)      # links to vector DB (long-term memory)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat()) # audit / lifecycle tracking
    last_accessed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat()) # supports expiry & cleanup