class PromptBuilder:

    @staticmethod
    def build_context(question: str, answer: str):
        """
        Returns structured context (NOT a string)
        """
        context = []

        # System instruction (single source of truth)
        context.append({
            "role": "system",
            "content": "You are a helpful AI assistant."
        })

        # User question
        context.append({
            "role": "user",
            "content": question
        })

        # Partial assistant answer (for autocomplete)
        if answer:
            context.append({
                "role": "assistant",
                "content": answer
            })

        return context

    @staticmethod
    def render(context):
        """
        Converts structured context into a prompt string
        """
        lines = []
        for msg in context:
            role = msg["role"].upper()
            lines.append(f"{role}: {msg['content']}")
        return "\n".join(lines)