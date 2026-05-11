from .context_validator import ContextValidator
from .injection_filter import InjectionFilter
from .pruning_strategy import PruningStrategy

# ContextIntegrityGuard is a Single entry point
# Nothing reaches LLM without passing here
class ContextIntegrityGuard: # Orchestrator – THE FIREWALL
    """
    Single entry firewall for PROMPT only
     NO semantic checks
     NO drift detection
    """

    def __init__(self, max_tokens=2048):
        self.validator = ContextValidator()
        self.injection_filter = InjectionFilter()
        self.pruner = PruningStrategy(max_tokens)

    def enforce(self, context: list, question: str):
        """
        Enforces prompt integrity BEFORE LLM call
        """

        # -------------------------------------------------
        # 🔥 RULE 1: NEVER block first turn
        # -------------------------------------------------
        if not context or not question:
            raise RuntimeError("Invalid prompt or question")

        # -------------------------------------------------
        # 1. Structural validation (format only)
        # -------------------------------------------------
        self.validator.validate(context)

        # -------------------------------------------------
        # 2. Prompt injection protection
        # -------------------------------------------------
        context = self.injection_filter.filter(context)

        # -------------------------------------------------
        # 3. Token-safe pruning
        # -------------------------------------------------
        context = self.pruner.prune(context)

        return context