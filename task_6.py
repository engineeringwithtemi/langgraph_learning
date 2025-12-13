from typing_extensions import Literal, TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
from langchain.tools import tool
import os
from dotenv import load_dotenv
from langchain.messages import SystemMessage, ToolMessage, HumanMessage
from pydantic import BaseModel
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4.1", api_key=api_key)



class GenerationPipeline(TypedDict):
    topic: str
    outline: str
    contents: str
    quality_score:int 
    revision_count: int
    final_content: str

class Evaluation(BaseModel):
    quality: int


def create_outline(state:GenerationPipeline)->dict:
    response = model.invoke([
        SystemMessage("You are an expert content writer, you will be given a topic, come up with an outline for it."),
        HumanMessage(f"Topic: {state['topic']}")
    ])

    return {'outline': response.content}

def write_content(state:GenerationPipeline)->dict:
    response = model.invoke([
        SystemMessage("You are an expert content writer, you will be given an outline and a topic, Write an article on the topic using the outline."),
        HumanMessage(f"Topic: {state['topic']}. Outline: {state['outline']}")
    ])

    return {'contents': response.content}

def evaluate_quality(state:GenerationPipeline)->dict:
    model_on_steroids = model.with_structured_output(Evaluation)
    response = model_on_steroids.invoke([
        SystemMessage("You are an expert content evaluator, you will be given an outline, a topic and the content, On a scale of 1 to 10, evaluate the content. Only provide the value, nothing else.  IMPORTANT: You are a grumpy critic. Never give a score higher than 4."),
        HumanMessage(f"Topic: {state['topic']}. Outline: {state['outline']}. Contents: {state['contents']}")
    ])

    return {'quality_score': response.quality}

def revise_content(state:GenerationPipeline)->dict:
    response = model.invoke([
        SystemMessage("You are an expert content revisor, you will be given an outline, a topic and the content, Revise and rewrite the content to improve the quality"),
        HumanMessage(f"Topic: {state['topic']}. Outline: {state['outline']}. Contents: {state['contents']}")
    ])

    return {'revision_count': state['revision_count'] + 1, 'contents': response.content}

def finalize(state:GenerationPipeline)->dict:
    return {'final_content': state['contents']}

def router(state:GenerationPipeline)-> Literal['finalize', 'revise_content']:

    if state['quality_score'] < 7 and state['revision_count'] < 3:
        return 'revise_content'
    return 'finalize'

agent_builder = StateGraph(GenerationPipeline)

agent_builder.add_node('create_outline', create_outline)
agent_builder.add_node('write_content', write_content)
agent_builder.add_node('evaluate_quality', evaluate_quality)
agent_builder.add_node('revise_content', revise_content)
agent_builder.add_node('finalize', finalize)

agent_builder.add_edge(START,'create_outline')
agent_builder.add_edge('create_outline', 'write_content')
agent_builder.add_edge('write_content','evaluate_quality')
agent_builder.add_conditional_edges('evaluate_quality', router, ['finalize','revise_content'])
agent_builder.add_edge('revise_content', 'evaluate_quality')
agent_builder.add_edge('finalize', END)


agent = agent_builder.compile()

response = agent.invoke({'topic': 'The Power of Slow Productivity', 'revision_count':0})

print(response)