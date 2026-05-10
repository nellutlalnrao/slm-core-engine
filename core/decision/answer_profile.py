from dataclasses import dataclass

@dataclass
class AnswerProfile:
    def __init__(self, length_type: str, max_tokens: int, chunk_tokens: int):
        self.length_type = length_type          # short | medium | long
        self.max_tokens = max_tokens
        self.chunk_tokens = chunk_tokens

    def __repr__(self):
        return (
            f"AnswerProfile(length_type={self.length_type}, "
            f"max_tokens={self.max_tokens}, "
            f"chunk_tokens={self.chunk_tokens})"
        )