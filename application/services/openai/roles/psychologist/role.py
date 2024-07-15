from dataclasses import dataclass

from langchain_core.prompts import BasePromptTemplate
from langchain_openai import ChatOpenAI

from application.core.enums import RoleEnum
from application.services.openai.roles.interfaces import AIRole
from application.services.openai.roles.psychologist.prompt import PROMPT


@dataclass
class Psychologist(AIRole):
    prompt: BasePromptTemplate
    role_id: RoleEnum
    llm: ChatOpenAI
    ai_prefix: str
    index_name: str = None
    data_file_name: str = None

    @staticmethod
    def load_role(user_language: str):
        prompt = PROMPT
        role_id = RoleEnum.PSYCHOLOGIST
        llm = ChatOpenAI(temperature="1", model="gpt-4o")
        ai_prefix = "Assistant"

        return Psychologist(
            prompt=prompt,
            role_id=role_id,
            llm=llm,
            ai_prefix=ai_prefix
        )