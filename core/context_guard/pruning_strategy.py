# PruningStrategy preserves system + active intent and drops least valuable history first
class PruningStrategy: # Token-Safe Emergency Control

    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    def prune(self, context):
        while self._estimate_tokens(context) > self.max_tokens:
            # Never remove system message
            for i, msg in enumerate(context):
                if msg["role"] not in ("system", "user"):
                    context.pop(i)
                    break
            else:
                break  # nothing left to prune safely

        return context

    def _estimate_tokens(self, context):
        # Approximation (safe + fast)
        return sum(len(m["content"].split()) for m in context)