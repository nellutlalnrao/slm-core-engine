from core.engine.prompt_builder import PromptBuilder
from core.completion.hard_stop import HardStop


class AutocompleteOrchestrator:

    def __init__(self, llm_engine):
        self.llm_engine = llm_engine

    def complete(self, question, profile):
        answer = ""
        used_tokens = 0

        while True:
            # -----------------------------------------
            # Build base prompt (existing behavior)
            # -----------------------------------------
            prompt = PromptBuilder.build(question, answer)

            # -----------------------------------------
            # Role-aware context injection
            # -----------------------------------------
            if hasattr(profile, "context_builder") and profile.context_builder:
                prompt = profile.context_builder.build(
                    profile.role,
                    prompt
                )

            # -----------------------------------------
            # Generate next chunk
            # -----------------------------------------
            chunk = self.llm_engine.generate(prompt, profile.chunk_tokens)
            answer += chunk
            used_tokens += profile.chunk_tokens

            # -----------------------------------------
            # Hard stop conditions
            # -----------------------------------------
            if HardStop.should_stop(answer, used_tokens, profile.max_tokens):
                break

        return answer.strip()