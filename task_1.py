from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class GreetingState(TypedDict):
    name: str
    greeting: str



def greet(state:GreetingState)-> GreetingState:

    return {'greeting': f"Hi {state['name']}! This is langgraph!"}



graph_builder = StateGraph(GreetingState)

graph_builder.add_node("greet", greet)
graph_builder.add_edge(START, "greet")
graph_builder.add_edge("greet", END)

graph = graph_builder.compile()


print(graph.invoke({'name': 'Alice'}))

"""
Lessons:
- start and end nodes can be implicitly defined by connecting edges to them
- The state is used by langgraph to keep all nodes in sync and it handles updating the state with values gotten from a node
- invoking a graph is basically setting values of the state
"""