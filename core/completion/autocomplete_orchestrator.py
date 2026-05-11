from core.engine.prompt_builder import PromptBuilder
from core.completion.hard_stop import HardStop
from core.context_guard.integrity_guard import ContextIntegrityGuard

class AutocompleteOrchestrator:

    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
        self.guard = ContextIntegrityGuard()   # FIREWALL INSTANCE

    def complete(self, question, profile):
        answer = ""
        used_tokens = 0

        while True:
            # -----------------------------------------
            # Build base prompt
            # -----------------------------------------
            context = PromptBuilder.build_context(question, answer)

            # -----------------------------------------
            # Role-aware context injection
            # -----------------------------------------
            if hasattr(profile, "context_builder") and profile.context_builder:
                context = profile.context_builder.build(
                    profile.role,
                    context
                )

            # -----------------------------------------
            # CONTEXT INTEGRITY GUARD
            # -----------------------------------------
            if answer:   # 🔥 RUN GUARD ONLY AFTER FIRST CHUNK
                try:
                    context = self.guard.enforce(
                        context=context,
                        question=question
                    )
                except Exception:
                    return "I cannot continue due to context inconsistency."

            # -----------------------------------------
            # FINAL STEP: RENDER TO STRING
            # -----------------------------------------
            prompt = PromptBuilder.render(context)

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