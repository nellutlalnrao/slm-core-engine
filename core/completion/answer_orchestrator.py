from core.decision.answer_length_decider import AnswerLengthDecider
from core.completion.autocomplete_orchestrator import AutocompleteOrchestrator

from core.role.role_detector import RoleDetector
from core.role.role_context_builder import RoleContextBuilder

from core.context_guard.drift_detector import DriftDetector

class AnswerOrchestrator:
    """
    Role-Aware Answer Orchestration

    Flow:
    1. Decide answer length
    2. Detect user role
    3. Build role-aware context
    4. Run autocomplete orchestration
    """
    def __init__(self, llm_engine,  session_manager=None):
        self.autocomplete = AutocompleteOrchestrator(llm_engine)
        self.session_manager = session_manager  # optional but recommended
        self.drift_detector = DriftDetector()

    def get_complete_answer(self, question: str, session_id: str = None) -> str:
        """
        Entry point expected by main.py
        Flow:
        1. Decide answer length
        2. Create answer profile
        3. Run autocomplete orchestration
        """
        # -------------------------------------------------
        # Decide answer length
        # -------------------------------------------------
        profile = AnswerLengthDecider.decide(question)

        # -------------------------------------------------
        # Detect role
        # -------------------------------------------------
        session_messages = []
        if self.session_manager and session_id:
            session = self.session_manager.get_session(session_id)
            session_messages = session.messages

        role = RoleDetector.detect(question, session_messages)

        # -------------------------------------------------
        # Inject role into profile/context
        # -------------------------------------------------
        profile.role = role
        profile.context_builder = RoleContextBuilder

        # -------------------------------------------------
        # Autocomplete with role-aware profile
        # -------------------------------------------------
        answer = self.autocomplete.complete(question, profile)

        # -------------------------------------------------
        # Drift detection ONLY on final answer
        # -------------------------------------------------
        try:
            self.drift_detector.check(question, answer)
        except RuntimeError:
            return "Answer halted due to topic inconsistency."

        return answer