# core/token/token_limiter.py

def decide_max_tokens(user_query: str) -> int:
    """
    Decide max tokens for LLM response based on query type.
    Phase-2.1: Token Limiter
    """

    if not user_query:
        return 50

    q = user_query.lower()
    word_count = len(q.split())

    if word_count < 5:
        return 50

    if any(k in q for k in ("explain", "why", "how")):
        return 150

    if any(k in q for k in ("code", "implement", "example")):
        return 200

    if any(k in q for k in ("architecture", "design", "system")):
        return 250

    return 120