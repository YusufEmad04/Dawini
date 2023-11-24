from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from classes import *

def init_agent(handler, session_id):
    with open("message.txt", encoding="utf-8") as f:
        sys_message = f.read()

    system_message = SystemMessage(content=sys_message)
    chat_history = MessagesPlaceholder(variable_name="chat_history")
    human_message = HumanMessagePromptTemplate.from_template("{question}")

    messages = [system_message, chat_history, human_message]

    template = ChatPromptTemplate.from_messages(messages=messages)

    reminder = "جاوب باللغة العربية اللهجة المصرية دائما"

    chain = LLMChain(
        verbose=True,
        prompt=template,
        llm=ChatOpenAI(temperature=0.2, model="gpt-4", streaming=True, callbacks=[handler]),
        memory=ConversationBufferMemory(max_token_limit=10000, memory_key="chat_history", return_messages=True, chat_memory=DynamoDBChatMessageHistoryNew(table_name="langchain-agents", session_id=session_id, reminder=reminder)),
    )

    return chain