from core.decision.answer_length_decider import AnswerLengthDecider
from core.completion.autocomplete_orchestrator import AutocompleteOrchestrator


class AnswerOrchestrator:

    def __init__(self, llm_engine):
        self.autocomplete = AutocompleteOrchestrator(llm_engine)

    def get_complete_answer(self, question: str) -> str:
        """
        Entry point expected by main.py
        Flow:
        1. Decide answer length
        2. Create answer profile
        3. Run autocomplete orchestration
        """
        profile = AnswerLengthDecider.decide(question)
        return self.autocomplete.complete(question, profile)