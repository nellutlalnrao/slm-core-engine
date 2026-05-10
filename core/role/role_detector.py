class RoleDetector:

    @staticmethod
    def detect(user_query: str, session_context: list) -> str:
        q = user_query.lower()

        if any(k in q for k in ["explain", "teach", "what is"]):
            return "student"

        if any(k in q for k in ["optimize", "architecture", "design", "system"]):
            return "developer"

        if any(k in q for k in ["summary", "decision", "compare", "pros", "cons"]):
            return "business"

        if any(k in q for k in ["debug", "error", "fix", "issue"]):
            return "debug"

        return "default"