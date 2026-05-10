class PriorityScorer:

    @staticmethod
    def score(message: str, role: str = "user") -> int:
        text = message.lower()

        # HIGH SIGNAL
        if any(k in text for k in ["remember", "always", "never", "important", "must"]):
            return 10

        if "?" in text:
            return 8

        if role == "assistant":
            return 6

        # LOW SIGNAL
        if len(text) < 10:
            return 2

        if text in ["ok", "okay", "thanks", "thank you"]:
            return 3

        # DEFAULT
        return 5