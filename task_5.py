from typing_extensions import Literal
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
from langchain.tools import tool
import os
from dotenv import load_dotenv
from langchain.messages import SystemMessage, ToolMessage, HumanMessage

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4.1", api_key=api_key)


@tool
def add(x: int, y: int) -> int:
    """A function that returns the sum of two numbers. Accepts two inputs
    x: int
    y: int
    """
    return x + y

@tool
def multiply(x: int, y: int) -> int:
    """A function that returns the multiplication of two numbers. Accepts two inputs
    x: int
    y: int
    """
    return x * y

@tool
def subtract(x: int, y: int) -> int:
    """A function that returns the subtraction of two numbers. Accepts two inputs
    x: int
    y: int
    """
    return x - y


tools = [add, subtract, multiply]
tools_by_name = {tool.name: tool for tool in tools}

model_with_tools = model.bind_tools(tools)


def llm_node(state:MessagesState) -> dict:
    """LLM decides whether to call a tool or not"""
    return {
        "messages":[
            model_with_tools.invoke([
                SystemMessage("You are an helpful assistant who uses the tools availabl to you to sovle maths questions from the user"),
            ] + 
            state['messages']
            
            )
        ]
    }

def tool_node(state:MessagesState) -> dict:
    """Executes the tool"""

    result = []

    for tool_call in state['messages'][-1].tool_calls:
        _tool = tools_by_name[tool_call['name']]
        observation = _tool.invoke(tool_call['args'])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call['id']))

    return {'messages': result}


def should_continue(state: MessagesState) -> Literal['tool_node', END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    last_message = state['messages'][-1]

    if last_message.tool_calls:
        return 'tool_node'
    return END

agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm_node", llm_node)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START,'llm_node')

agent_builder.add_conditional_edges('llm_node', should_continue, ['tool_node', END])
agent_builder.add_edge('tool_node', 'llm_node')

agent = agent_builder.compile()

messages = [HumanMessage(content="Add 3 and 4.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()

