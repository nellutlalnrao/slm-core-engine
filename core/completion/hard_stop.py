class HardStop:

    @staticmethod
    def should_stop(accumulated_text: str, used_tokens: int, max_tokens: int) -> bool:
        if used_tokens >= max_tokens:
            return True

        if accumulated_text.strip().endswith((".", "!", "?")):
            return True

        return False