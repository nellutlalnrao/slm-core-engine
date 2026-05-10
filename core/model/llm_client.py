class LLMClient:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, prompt, max_tokens=150):
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.6,
            top_p=0.9,
            stop=["<|user|>", "<|assistant|>"]
        )
        return output["choices"][0]["text"].strip()