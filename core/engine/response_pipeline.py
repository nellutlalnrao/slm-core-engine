from core.decision.answer_length_decider import AnswerLengthDecider
from core.completion.answer_orchestrator import AnswerOrchestrator


class ResponsePipeline:

    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
        self.answer_orchestrator = AnswerOrchestrator(llm_engine)

    def run(self, question: str) -> str:
        profile = AnswerLengthDecider.decide(question)
        return self.answer_orchestrator.answer(question, profile)