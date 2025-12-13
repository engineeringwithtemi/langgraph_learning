from typing_extensions import Literal, TypedDict, Annotated
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
from langchain.tools import tool
import os
from dotenv import load_dotenv
from langchain.messages import SystemMessage, ToolMessage, HumanMessage, AIMessage
from pydantic import BaseModel
import operator
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4.1", api_key=api_key)


class ChatMessages(MessagesState):
    messages: Annotated[list, operator.add]


def chat_node(state:ChatMessages)-> ChatMessages:
    prompt = "You are a helpful chatbot. You have context of all the previous conversations with a user and you respond to the user based on the conversation."

    response = model.invoke(
        [SystemMessage(prompt)]
        + state['messages']
    )
    return {'messages':[AIMessage(response.content)]}


checkpointer = InMemorySaver()

agent_builder = StateGraph(ChatMessages)

agent_builder.add_node("chat_node", chat_node)
agent_builder.add_edge(START, "chat_node")
agent_builder.add_edge("chat_node", END)

chat_agent = agent_builder.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "1",}}

print(chat_agent.invoke({
    'messages':[HumanMessage("My name is Bob")]
}, config=config))

print(chat_agent.invoke({
    'messages':[HumanMessage("What is my name ?")]
}, config=config))

print(chat_agent.invoke({
    'messages':[HumanMessage("Tell me a joke about my name ?")]
}, config=config))

