from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4.1", api_key=api_key)



class WritingState(TypedDict):
    outline: str
    draft: str
    edit: str
    topic: str

def outline(state:WritingState)-> dict:
    return {'outline': "The outline is 1. Outline 1, 2. outline 2"}

def draft(state:WritingState)-> dict:
    return {'draft': "This is the draft of the outline."}

def edit(state:WritingState)-> dict:
    return {'edit': "This is the edit of the outline."}

writing_graph_builder = StateGraph(WritingState)
writing_graph_builder.add_node('outline', outline)
writing_graph_builder.add_node('draft', draft)
writing_graph_builder.add_node('edit', edit)


writing_graph_builder.add_edge(START, "outline")
writing_graph_builder.add_edge("outline", "draft")
writing_graph_builder.add_edge("draft", "edit")
writing_graph_builder.add_edge('edit', END)

writing_agent = writing_graph_builder.compile()

class ResearchState(TypedDict):
    search: str
    summarize: str
    validate: str


def search(state:ResearchState)-> dict:
    return {'search': "The outline is 1. Outline 1, 2. outline 2"}

def summarize(state:ResearchState)-> dict:
    return {'summarize': "This is the summary of the outline."}

def validate(state:ResearchState)-> dict:
    return {'validate': "This is the edit of the outline."}



research_graph_builder = StateGraph(ResearchState)
research_graph_builder.add_node('search', search)
research_graph_builder.add_node('summarize', summarize)
research_graph_builder.add_node('validate', validate)

research_graph_builder.add_edge(START, "search")
research_graph_builder.add_edge("search", "summarize")
research_graph_builder.add_edge("summarize", "validate")
research_graph_builder.add_edge('validate', END)
research_agent = research_graph_builder.compile()


class ParentState(TypedDict):
    topic: str
    result: str
    final: str


def call_research(state:ParentState):
    result = research_agent.invoke({'search': state['topic']})
    return {'result': result['summarize']}

def call_writer(state: ParentState):
    result = writing_agent.invoke({'topic': state['result']})
    return {'final': result['edit']}


parent_builder = StateGraph(ParentState)
parent_builder.add_node("call_research", call_research)
parent_builder.add_node("call_writer", call_writer)
parent_builder.add_edge(START, "call_research")
parent_builder.add_edge("call_research", "call_writer")
parent_builder.add_edge("call_writer", END)
parent_graph = parent_builder.compile()


print(parent_graph.invoke({'topic': 'State of earth'}))