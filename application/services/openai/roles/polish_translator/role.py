from dataclasses import dataclass

from langchain_core.prompts import BasePromptTemplate
from langchain_openai import ChatOpenAI

from application.core.enums import RoleEnum
from application.services.openai.roles.interfaces import AIRole
from application.services.openai.roles.polish_translator.prompt import get_translator_prompt


@dataclass
class PolishTranslator(AIRole):
    prompt: BasePromptTemplate
    role_id: RoleEnum
    llm: ChatOpenAI
    ai_prefix: str
    index_name: str = None
    data_file_name: str = None

    @staticmethod
    def load_role(user_language: str):
        prompt = get_translator_prompt(user_language)
        role_id = RoleEnum.POLISH_TRANSLATOR
        llm = ChatOpenAI(temperature="0.7", model="gpt-4o", max_tokens="460")
        ai_prefix = "Translator"

        return PolishTranslator(
            prompt=prompt,
            role_id=role_id,
            llm=llm,
            ai_prefix=ai_prefix
        )