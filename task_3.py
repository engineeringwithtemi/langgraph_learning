from typing_extensions import Literal, TypedDict
from langgraph.graph import StateGraph, START, END



class OddEvenState(TypedDict):
    result: str
    number: int
    path_taken: str


def check_number(state:OddEvenState)-> Literal['odd_node', 'even_node']:
    if state['number'] % 2 == 0:
        return "even_node"
    else:
        return "odd_node"
    

def handle_even(state:OddEvenState) -> OddEvenState:
    return {'result': f"Even number: {state['number']}", 'path_taken': "even_node"}

def handle_odd(state:OddEvenState) -> OddEvenState:
    return {'result': f"Odd number: {state['number']}", 'path_taken': "odd_node"}


agent_builder = StateGraph(OddEvenState)


agent_builder.add_node('handle_even', handle_even)
agent_builder.add_node('handle_odd', handle_odd)

agent_builder.add_conditional_edges(START, check_number, {
    'even_node': "handle_even",
    'odd_node': "handle_odd"
})

agent_builder.add_edge('handle_even', END)
agent_builder.add_edge('handle_odd', END)


agent = agent_builder.compile()


print(agent.invoke({'number': 4}))
