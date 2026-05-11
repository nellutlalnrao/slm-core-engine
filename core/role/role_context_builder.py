# core/role/role_context_builder.py

class RoleContextBuilder:

    @staticmethod
    def build(role, context):
        """
        Inject role instruction into structured context.
        Input:  context -> list of {role, content}
        Output: context -> list of {role, content}
        """

        if not role or not context:
            return context

        # Merge role into existing system message
        if context[0]["role"] == "system":
            context[0]["content"] += f" You are acting as a {role}."
            return context

        return context