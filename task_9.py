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
import time
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4.1", api_key=api_key)



class ResearchAssistant(TypedDict):
    query: str
    web_results: str
    academic_results: str
    news_results: str
    combined: str

def search_web(state:ResearchAssistant) -> dict:
    time.sleep(1)
    return {'web_results': 'Result of the web'}

def academic_result(state:ResearchAssistant) -> dict:
    time.sleep(1.5)
    return {'academic_results': 'Academic Results'}

def news_result(state:ResearchAssistant) -> dict:
    time.sleep(.5)
    return {'news_results': "Result of news"}

def combine_result(state:ResearchAssistant) -> dict:
    return {'combined': f"The result of the search query={state['query']} are {state['web_results']} for web, {state['news_results']} for news and {state['academic_results']} for academic."}

agent_builder = StateGraph(ResearchAssistant)

agent_builder.add_node("search_web",search_web )
agent_builder.add_node("academic_result",academic_result )
agent_builder.add_node("news_result",news_result )
agent_builder.add_node("combine_result",combine_result )

agent_builder.add_edge(START, 'search_web')
agent_builder.add_edge(START, 'academic_result')
agent_builder.add_edge(START, 'news_result')

agent_builder.add_edge("search_web", 'combine_result')
agent_builder.add_edge("academic_result", 'combine_result')
agent_builder.add_edge("news_result", 'combine_result')

agent_builder.add_edge("combine_result", END)


agent = agent_builder.compile()
start = time.time()
result = agent.invoke({'query': "What is the state of the world."})
elapsed = time.time() - start
print(f"Total time: {elapsed:.2f}s (should be ~1.5s if parallel)")
print(result['combined'])
