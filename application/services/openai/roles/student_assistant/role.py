from dataclasses import dataclass

from langchain_core.prompts import BasePromptTemplate
from langchain_openai import ChatOpenAI

from application.core.enums import RoleEnum
from application.services.openai.roles.interfaces import AIRole
from application.services.openai.roles.student_assistant.prompt import PROMPT


@dataclass
class StudentAssistant(AIRole):
    prompt: BasePromptTemplate
    role_id: RoleEnum
    llm: ChatOpenAI
    ai_prefix: str
    index_name: str
    data_file_name: str

    @staticmethod
    def load_role(user_language: str):
        prompt = PROMPT
        index_name = "agent-adaptation"
        role_id = RoleEnum.STUDENT_ASSISTANT
        data_file_name = "agent_adaptation.pdf"
        llm = ChatOpenAI(temperature="0", model="gpt-4o")
        ai_prefix = "Assistant"

        return StudentAssistant(
            prompt=prompt,
            index_name=index_name,
            role_id=role_id,
            data_file_name=data_file_name,
            llm=llm,
            ai_prefix=ai_prefix
        )