from core.role.role_profiles import ROLE_PROFILES

class RoleContextBuilder:

    @staticmethod
    def build(role: str, base_context: str) -> str:
        profile = ROLE_PROFILES.get(role, ROLE_PROFILES["default"])

        role_instruction = f"""
You are operating in ROLE: {role}

Style Guide:
- Tone: {profile['style']}
- Verbosity: {profile['verbosity']}

Follow role strictly while answering.
"""

        return role_instruction + "\n\n" + base_context