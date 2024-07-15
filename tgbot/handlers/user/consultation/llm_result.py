from dataclasses import dataclass

from application.services.openai.roles.interfaces import AIRole


@dataclass
class LLMResults:
    text: str
    ai_role: AIRole
