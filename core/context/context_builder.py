class ContextBuilder:
    def __init__(self, session_manager, max_messages=10):
        self.session_manager = session_manager
        self.max_messages = max_messages

    def build(self, session):
        # Get messages via SessionManager (correct source of truth)
        messages = self.session_manager.get_messages(session)

        # Take only last N messages
        recent = messages[-self.max_messages:]

        context_lines = []
        for msg in recent:
            context_lines.append(f"{msg.role.upper()}: {msg.content}")

        return "\n".join(context_lines)