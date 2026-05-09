import uuid
from core.session.models import Session, Message
from core.session.session_store import SessionStore

MAX_RECENT_MESSAGES = 10   # sliding window

# Session Controller (Brain Gatekeeper) - Controls creation, retrieval, and mutation of sessions.
# What it does?
#   a) Creates a new session when none exists
#   b) Loads an existing session using session_id
#   c) Appends messages to the session
#   d) Enforces sliding window limits
#   e) Saves session after every update

class SessionManager:

    def get_or_create(self, user_id: str, session_id: str | None = None) -> Session: # guarantees session existence
        if session_id:
            session = SessionStore.load(session_id)
            if session and session.user_id == user_id:
                return session

        session = Session(
            session_id=str(uuid.uuid4()),
            user_id=user_id
        )
        SessionStore.save(session)
        return session

    def add_message(self, session: Session, role: str, content: str): # appends message, trims old messages, persists state
        session.recent_messages.append(Message(role, content))

        # Sliding window
        if len(session.recent_messages) > MAX_RECENT_MESSAGES:
            session.recent_messages = session.recent_messages[-MAX_RECENT_MESSAGES:]

        SessionStore.save(session)

    def get_context_payload(self, session: Session) -> dict:
        return {
            "summary": session.summary,
            "recent_messages": [
                {"role": m.role, "content": m.content}
                for m in session.recent_messages
            ]
        }