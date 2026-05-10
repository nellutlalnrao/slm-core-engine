from core.completion.completion_checker import CompletionChecker
from core.token.token_limiter import decide_max_tokens

# AnswerOrchestrator: The Heart of the AutoComplete Orchestration Feature.

class AnswerOrchestrator:

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def get_complete_answer(self, question: str) -> str:
        collected = ""

        prompt = (
            "<|user|>\n"
            f"{question}\n"
            "<|assistant|>\n"
        )

        for _ in range(10):  # safety cap
            max_tokens = min(decide_max_tokens(question), 300)
            chunk = self.llm_client.generate(prompt)
            collected += "\n" + chunk

            if CompletionChecker.is_complete(collected):
                break
            
            # Answer Continuation:
            # We do NOT merge chunks by trusting the model. We merge chunks by controlling the continuation context.
            # "Continue the previous answer from where it stopped. Do not repeat. Do not restart numbering." - tells the model: 
            #   a) Same answer 
            #   b) Same list 
            #   c) Same structure
            prompt = (
                "<|system|>\n"
                "Continue the previous answer from where it stopped. "
                "Do not repeat. Do not restart numbering.\n"
                "<|assistant|>\n"
                f"{collected}\n"
            )

        return collected.strip()