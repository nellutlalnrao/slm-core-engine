from core.engine.prompt_builder import PromptBuilder
from core.completion.hard_stop import HardStop


class AutocompleteOrchestrator:

    def __init__(self, llm_engine):
        self.llm_engine = llm_engine

    def complete(self, question, profile):
        answer = ""
        used_tokens = 0

        while True:
            prompt = PromptBuilder.build(question, answer)
            chunk = self.llm_engine.generate(prompt, profile.chunk_tokens)

            answer += chunk
            used_tokens += profile.chunk_tokens

            if HardStop.should_stop(answer, used_tokens, profile.max_tokens):
                break

        return answer.strip()