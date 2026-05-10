import uuid
from core.session.models import Session, Message
from core.session.session_store import SessionStore

from core.memory.priority_scorer import PriorityScorer
from core.memory.signal_classifier import tag_message

MAX_RECENT_MESSAGES = 10   # sliding window


# Session Manager (Brain Gatekeeper)
# Responsibilities:
#   a) Create or load sessions
#   b) Append messages to sessions
#   c) Enforce sliding window memory
#   d) Persist session state
#   e) Expose session data safely to other components (ContextBuilder, Summarizer)

class SessionManager:

    def __init__(self):
        # In-memory cache (optional, future use)
        # session_id -> Session object
        self.sessions = {}

    def get_or_create(
        self,
        user_id: str,
        session_id: str | None = None
    ) -> Session:
        """
        Guarantees a valid session.
        - Loads existing session if session_id is provided and valid
        - Otherwise creates a new session
        """

        if session_id:
            session = SessionStore.load(session_id)
            if session and session.user_id == user_id:
                self.sessions[session.session_id] = session
                return session

        # Create new session
        session = Session(
            session_id=str(uuid.uuid4()),
            user_id=user_id
        )

        SessionStore.save(session)
        self.sessions[session.session_id] = session
        return session

    def add_message(
        self,
        session: Session,
        role: str,
        content: str
    ):
        """
        Appends a message to the session.
        Enforces sliding window.
        Persists session after update.
        """
        # Enrichment layer
        priority = PriorityScorer.score(content, role)
        tags = tag_message(content)

        # Enhanced message object
        message = Message(
            role=role,
            content=content
        )

        # Attach dynamic metadata (safe extension)
        message.priority = priority
        message.tags = tags

        session.recent_messages.append(
            Message(role=role, content=content)
        )

        # Sliding window enforcement
        if len(session.recent_messages) > MAX_RECENT_MESSAGES:
            session.recent_messages = session.recent_messages[-MAX_RECENT_MESSAGES:]

        SessionStore.save(session)

    def get_messages(self, session: Session):
        """
        Read-only accessor used by ContextBuilder.
        Returns recent messages stored inside the session.
        """

        return session.recent_messages

    def get_context_payload(self, session: Session) -> dict:
        """
        Structured payload for future phases:
        - Phase-2.2 summarization
        - Phase-2.3 priority memory
        - Phase-3 vector memory
        """

        return {
            "summary": session.summary,
            "recent_messages": [
                {
                    "role": m.role,
                    "content": m.content
                }
                for m in session.recent_messages
            ]
        }