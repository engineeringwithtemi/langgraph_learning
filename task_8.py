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

class EmailState(TypedDict):
  recipient: str
  draft: str
  approved: bool
  sent: bool
  subject: str


def draft_node(state:EmailState)-> dict:
  response = model.invoke([
    SystemMessage("You're an executive assistant that help in managing the inbox of your client. You handle things like drafting emails, replying emails etc."),
    HumanMessage(f"Draft an email to {state['recipient']} informing them about upcoming changes in their billing for the plumbing service they provide from {state['subject']}")
  ])

  return {'draft': response.content}

def send_email(state:EmailState) -> dict:
  print(f"Email: {state['draft']} sent to {state['recipient']} from {state['subject']}.")
  return {'sent': True}

memory = InMemorySaver()

agent_builder = StateGraph(EmailState)
agent_builder.add_node("draft_node", draft_node)
agent_builder.add_node("send_email", send_email)

agent_builder.add_edge(START, 'draft_node')
agent_builder.add_edge('draft_node', 'send_email')
agent_builder.add_edge('send_email', END)

graph = agent_builder.compile(checkpointer=memory, interrupt_before=["send_email"])

thread = {'configurable':{'thread_id': '1'}}
print(graph.invoke({
  'recipient': 'test@gmail.com',
  'subject': "user@test.com",
  'draft': "",
  'approved': False,
  'sent': False
}, thread))


print(graph.update_state(thread, {'approved': True}))

graph.invoke(None, thread)

print(graph.get_state(thread).values)

