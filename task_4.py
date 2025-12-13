from typing_extensions import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4.1", api_key=api_key)

class ChatAgentState(TypedDict):
    topic: str
    draft: str
    final: str


def generate_draft(state:ChatAgentState)-> ChatAgentState:
    # Define prompt with input variable
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a expert writer who drafts articles based on a topic."),
        ("human", "{message}")
    ])

    prompt_value = prompt.invoke(f"Write an article on {state['topic']}")

    response = model.invoke(prompt_value)
    return {'draft': response.content}

def polish_draft(state:ChatAgentState) -> ChatAgentState:
     # Define prompt with input variable
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a expert writer who finalises an article from draft to a final copy. You ensure it's of high quality."),
        ("human", "{message}")
    ])

    prompt_value = prompt.invoke(f"Finalise this draft \n {state['draft']}")

    response = model.invoke(prompt_value)
    return {'final': response.content}


agent_builder = StateGraph(ChatAgentState)

agent_builder.add_node("generate_draft", generate_draft )
agent_builder.add_node("polish_draft", polish_draft )

agent_builder.add_edge(START, "generate_draft")
agent_builder.add_edge("generate_draft", "polish_draft")
agent_builder.add_edge("polish_draft", END)

agent = agent_builder.compile()

print(agent.invoke({'topic': 'Langchain and Langgraph Changing the ecosystem.'}))