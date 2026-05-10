class MemoryFilter:

    def __init__(self, threshold=5):
        self.threshold = threshold

    def filter(self, messages):
        return [
            m for m in messages
            if getattr(m, "priority", 5) >= self.threshold
        ]