import re

class CompletionChecker:

    END_PATTERN = re.compile(r"(?:\bEND\b[!\s]*)+$", re.IGNORECASE)

    @staticmethod
    def normalize(text: str) -> str:
        """
        Remove trailing END / END! / END END noise
        but keep END if it appears in the middle.
        """
        text = text.rstrip()
        text = CompletionChecker.END_PATTERN.sub("", text).rstrip()
        return text

    @staticmethod
    def is_complete(text: str) -> bool:
        if not text:
            return False

        # Normalize trailing END spam first
        text = CompletionChecker.normalize(text)

        # 1. Very short answers are never complete
        if len(text) < 80:
            return False

        # 2. Obvious cut-offs
        if text.endswith((",", "and", "or", "...", "-")):
            return False

        lines = text.splitlines()
        last_line = lines[-1].strip()

        # 3. Detect unfinished numbered lists (1., 2., 3.)
        numbered = [
            int(m.group(1)) for line in lines
            if (m := re.match(r"\s*(\d+)\.", line))
        ]

        if numbered:
            # If last line is a list item → incomplete
            if re.match(r"\s*\d+\.", last_line):
                return False

        # 4. Detect unfinished sublists (a., b., c.)
        if re.match(r"\s*[a-zA-Z]\.", last_line):
            return False

        # 5. Strong completion signal: proper sentence ending
        if not last_line.endswith((".", "!", "?")):
            return False

        # 6. Heuristic: closing language (soft signal)
        closing_phrases = (
            "in summary",
            "overall",
            "as a result",
            "this concludes",
            "you can now",
            "happy coding",
        )

        if not any(p in text.lower() for p in closing_phrases):
            return False

        return True