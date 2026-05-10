class ContextTrimmer: # Reduces Token Size
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    def trim(self, messages):
        tokens = 0
        trimmed = []

        for msg in reversed(messages):
            msg_tokens = len(msg["content"].split())
            if tokens + msg_tokens > self.max_tokens:
                break
            trimmed.insert(0, msg)
            tokens += msg_tokens

        return trimmed