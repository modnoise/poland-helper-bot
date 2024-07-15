from dataclasses import dataclass

from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.core.enums import RoleEnum
from application.services.openai.memory.memory import ConversationSummaryBufferMemoryAsync
from application.services.openai.roles.interfaces import AIRole
from domain import Message
from application.services.openai.chat_history import SQLChatMessageHistory


@dataclass
class LLMArgs:
    ai_role: AIRole
    messages: list[Message]
    session_id: str
    question: str
    language: str
    session_pool: async_sessionmaker


async def run_llm(llm_args: LLMArgs) -> str:
    message_history = SQLChatMessageHistory(
        session_id=llm_args.session_id,
        session_pool=llm_args.session_pool,
        message_history=llm_args.messages,
        role_id=llm_args.ai_role.role_id
    )

    memory = ConversationSummaryBufferMemoryAsync(
        llm=ChatOpenAI(temperature="0", model="gpt-3.5-turbo"),
        max_token_limit=1000,
        ai_prefix=llm_args.ai_role.ai_prefix,
        chat_memory=message_history,
    )

    history_dict = await memory.prep_history()
    chain = LLMChain(
        llm=llm_args.ai_role.llm,
        prompt=llm_args.ai_role.prompt,
    )

    if llm_args.ai_role.role_id == RoleEnum.POLISH_TRANSLATOR:
        response = await chain.arun({"input": llm_args.question, "history": history_dict["history"]})
    else:
        response = await chain.arun(
            {"input": llm_args.question, "history": history_dict["history"], "language": llm_args.language})

    await memory.save_context({"input": llm_args.question}, {"response": response})
    return response
