from core.context.context_trimmer import ContextTrimmer
from core.context.context_summarizer import ContextSummarizer

from core.memory.memory_filter import MemoryFilter

class ContextBuilder:
    def __init__(
        self,
        session_manager,
        max_prompt_tokens=3500,
        recent_window=6,
        min_priority=5   # control knob
    ):
        self.session_manager = session_manager
        self.recent_window = recent_window
        self.min_priority = min_priority
        self.trimmer = ContextTrimmer(max_prompt_tokens)
        self.summarizer = ContextSummarizer()
        # Memory filter instance
        self.memory_filter = MemoryFilter(threshold=self.min_priority)

    def build(self, session):
        # 1. Source of truth remains SessionManager
        messages = self.session_manager.get_messages(session)

        if not messages:
            return ""

        # APPLY MEMORY FILTER (REAL USAGE)
        filtered_messages = self.memory_filter.filter(messages)

        # fallback safety
        if not filtered_messages:
            filtered_messages = messages

        # 2. Sliding window
        recent_messages = messages[-self.recent_window:]
        old_messages = messages[:-self.recent_window]

        # 3. Summarize old messages (Phase 2.2)
        if old_messages:
            summary = self.summarizer.summarize(old_messages)
            session.context_summary = summary
        else:
            summary = getattr(session, "context_summary", None)

        print(
            "Recent:", len(recent_messages),
            "| Summary exists:", bool(summary)
        )

        # 4. Build structured context
        context_blocks = []

        if summary:
            context_blocks.append({
                "role": "system",
                "content": f"Context Summary:\n{summary}"
            })

        for msg in recent_messages:
            context_blocks.append({
                "role": msg.role,
                "content": msg.content
            })

        # 5. Hard trim to token budget
        trimmed_context = self.trimmer.trim(context_blocks)

        # 6. Convert to prompt string (Phi-3 format)
        prompt_lines = []
        for msg in trimmed_context:
            prompt_lines.append(msg["content"])

        return "\n".join(prompt_lines)