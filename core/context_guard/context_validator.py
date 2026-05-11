# ContextValidator ensures exactly one system role and prevents malformed context
class ContextValidator: # Structure & Role Safety

    REQUIRED_ORDER = ["system", "memory", "user", "assistant"]

    def validate(self, context):
        if not context or not isinstance(context, list):
            raise ValueError("Context must be a non-empty list")

        self._validate_roles(context)
        self._validate_order(context)

    def _validate_roles(self, context):
        system_count = sum(1 for m in context if m["role"] == "system")
        if system_count != 1:
            raise ValueError("Context must contain exactly ONE system role")

    def _validate_order(self, context):
        last_index = -1
        for msg in context:
            role = msg.get("role")
            if role not in self.REQUIRED_ORDER:
                raise ValueError(f"Invalid role detected: {role}")

            index = self.REQUIRED_ORDER.index(role)
            if index < last_index:
                raise ValueError("Invalid role ordering in context")

            last_index = index