from core.decision.answer_profile import AnswerProfile

class AnswerLengthDecider:

    @staticmethod
    def decide(question: str) -> AnswerProfile:
        q = question.lower().strip()

        if len(q) < 40:
            return AnswerProfile("short", max_tokens=150, chunk_tokens=80)

        if any(word in q for word in ["explain", "describe", "why", "how"]):
            return AnswerProfile("medium", max_tokens=400, chunk_tokens=120)

        return AnswerProfile("long", max_tokens=800, chunk_tokens=150)