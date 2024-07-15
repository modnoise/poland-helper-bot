from abc import ABC

from langchain_core.prompts import BasePromptTemplate
from langchain_openai import ChatOpenAI

from application.core.enums import RoleEnum


class AIRole(ABC):
    prompt: BasePromptTemplate
    role_id: RoleEnum
    llm: ChatOpenAI
    ai_prefix: str
    data_file_name: str = None
    index_name: str = None

    @staticmethod
    def load_role(user_language: str):
        pass