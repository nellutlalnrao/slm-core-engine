class LLMEngine:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, prompt: str, max_tokens: int) -> str:
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=None
        )
        return response["choices"][0]["text"]