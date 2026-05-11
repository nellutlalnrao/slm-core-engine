# DriftDetector prevents answer restarting and prevents topic switching mid-answer
class DriftDetector: # Answer Continuity & Topic Guard

    def check(self, question: str, partial_answer: str):
        # -----------------------------------------
        # 0. FIRST TURN SAFETY (CRITICAL)
        # -----------------------------------------
        # Drift is impossible without stable context
        if not question or not partial_answer:
            return
        
        # -----------------------------------------
        # 1. No drift check for very short answers
        # -----------------------------------------
        if len(partial_answer.split()) < 25:
            return

        # -----------------------------------------
        # 2. No drift check if answer seems unfinished
        # -----------------------------------------
        if not partial_answer.strip().endswith((".", "!", "?")):
            return

        # -----------------------------------------
        # 3. Extract keywords
        # -----------------------------------------
        q_keywords = self._keywords(question)
        a_keywords = self._keywords(partial_answer)

        # -----------------------------------------
        # 4. Allow factual one-word / noun answers
        # -----------------------------------------
        if len(a_keywords) <= 2:
            return

        # -----------------------------------------
        # 5. Drift only if ZERO overlap after stability
        # -----------------------------------------
        if q_keywords and a_keywords and not q_keywords.intersection(a_keywords):
            raise RuntimeError("Context drift detected")

    def _keywords(self, text: str):
        return {
            w.lower()
            for w in text.split()
            if len(w) > 4
        }