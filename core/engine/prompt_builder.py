class PromptBuilder:

    @staticmethod
    def build(question: str, previous_answer: str = "") -> str:
        if not previous_answer:
            return f"Answer the following question clearly:\n{question}\nAnswer:"

        return (
            "Continue the answer naturally from where it stopped.\n\n"
            f"Previous answer:\n{previous_answer}\n\nContinue:"
        )