from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class SequentialPipeline(TypedDict):
    text: str
    cleaned: str
    analysed: str
    summarized: str


def clean_text(state:SequentialPipeline) -> dict[str, str]:
    return {'cleaned': state['text'].strip().lower()}

def analyse_text(state:SequentialPipeline) -> dict[str, str]:
    return {"analysed": f"{len(state['cleaned'].split(' '))} words, {len(state['cleaned'])} characters"}

def summarize(state:SequentialPipeline) -> dict[str, str]:
    return {"summarized": f"{state['analysed']} with cleaned text '{state['cleaned']}'"}


agent_builder = StateGraph(SequentialPipeline)

agent_builder.add_node("cleaned", clean_text)
agent_builder.add_node("analysed", analyse_text)
agent_builder.add_node("summarized", summarize)

agent_builder.add_edge(START, 'cleaned')
agent_builder.add_edge('cleaned','analysed')
agent_builder.add_edge('analysed','summarized')
agent_builder.add_edge('summarized', END)

agent = agent_builder.compile()

print(agent.invoke({'text': " Hello WORLD this is a TEST "}))