# InjectionFilter neutralizes role-breaking attempts and does NOT silently allow malicious content
class InjectionFilter: # Prompt Injection Firewall

    BLOCKED_PHRASES = [
        "ignore previous instructions",
        "you are now system",
        "act as system",
        "act as developer",
        "override system",
        "disregard above"
    ]

    def filter(self, context):
        for msg in context:
            if msg["role"] == "user":
                lowered = msg["content"].lower()
                for phrase in self.BLOCKED_PHRASES:
                    if phrase in lowered:
                        msg["content"] = "[POTENTIAL PROMPT INJECTION DETECTED]"
                        break
        return context