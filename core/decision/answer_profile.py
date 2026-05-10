from dataclasses import dataclass
from typing import Optional, Type

@dataclass
class AnswerProfile:
    length_type: str           # short | medium | long
    max_tokens: int
    chunk_tokens: int
    role: str = "default"
    context_builder: Optional[Type] = None

    def __init__(self, length_type: str, max_tokens: int, chunk_tokens: int, role: str = "default",
        context_builder: Optional[Type] = None):
        self.length_type = length_type          # short | medium | long
        self.max_tokens = max_tokens
        self.chunk_tokens = chunk_tokens
        self.role = role
        self.context_builder = context_builder

    def __repr__(self):
        return (
            f"AnswerProfile(length_type={self.length_type}, "
            f"max_tokens={self.max_tokens}, "
            f"chunk_tokens={self.chunk_tokens})"
            f"role={self.role})"
        )