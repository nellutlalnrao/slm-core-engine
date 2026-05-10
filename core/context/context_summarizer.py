# ContextSummarizer is rule-based first (safe, fast, deterministic)
class ContextSummarizer: # Compresses History
    def summarize(self, messages):
        important = []

        for m in messages:
            if m.role == "user":
                important.append(m.content)

        summary = " | ".join(important[-5:])
        return summary