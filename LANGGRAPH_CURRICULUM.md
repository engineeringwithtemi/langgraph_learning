# 🎓 LangGraph Learning Curriculum

> **Learning Mode**: You implement, I provide specs. No code from me—just clear requirements and acceptance criteria for each task.

---

## 📚 Curriculum Overview

This curriculum takes you from LangGraph fundamentals to advanced multi-agent architectures through **12 hands-on tasks** organized into 4 levels.

| Level | Focus | Tasks |
|-------|-------|-------|
| 🟢 Beginner | Core concepts & basic graphs | Tasks 1-3 |
| 🟡 Intermediate | Workflows & tool integration | Tasks 4-6 |
| 🟠 Advanced | State management & human-in-the-loop | Tasks 7-9 |
| 🔴 Expert | Multi-agent & production patterns | Tasks 10-12 |

---

## 📖 Key LangGraph Concepts Reference

Before diving into tasks, here are the core concepts you'll use throughout:

### Core Building Blocks
- **StateGraph**: The main class for building graphs. Takes a State type as input.
- **State**: A TypedDict defining what data flows through your graph
- **Nodes**: Python functions that transform state
- **Edges**: Connections between nodes (can be conditional)
- **START/END**: Special nodes marking entry and exit points

### Key Imports
```python
from langgraph.graph import StateGraph, MessagesState, START, END
from typing_extensions import TypedDict, Annotated
import operator
```

### Documentation Links
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [Workflows & Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

---

# 🟢 Level 1: Beginner

## Task 1: Hello LangGraph
> **Pattern**: Basic State Machine (Graph)
> **Type**: Flow Engineering

### Objective
Build your first LangGraph that greets a user by name.

### Requirements
1. Create a `State` TypedDict with fields:
   - `name: str` - the user's name
   - `greeting: str` - the generated greeting
   
2. Create a single node called `greet` that:
   - Reads the `name` from state
   - Returns a greeting like "Hello, {name}! Welcome to LangGraph."
   
3. Build the graph:
   - Add the `greet` node
   - Connect: `START` → `greet` → `END`
   - Compile and invoke with `{"name": "Alice"}`

### Acceptance Criteria
- [ ] State is properly defined as a TypedDict
- [ ] Graph compiles without errors
- [ ] Invoking with `{"name": "Alice"}` returns state with a greeting containing "Alice"
- [ ] Print the final state to verify output

### Hints
- Use `StateGraph(State)` to create the graph
- Nodes are just functions: `def greet(state: State) -> dict`
- Return only the fields you want to update

---

## Task 2: Sequential Pipeline
> **Pattern**: Chain / Pipeline (DAG)
> **Type**: Flow Engineering

### Objective
Build a 3-node pipeline that processes text through multiple transformations.

### Requirements
1. Create a `State` with fields:
   - `text: str` - original text
   - `cleaned: str` - after cleaning
   - `analyzed: str` - after analysis
   - `summary: str` - final summary

2. Create three nodes:
   - `clean_text`: Remove extra whitespace, lowercase the text
   - `analyze_text`: Count words and characters, add to state
   - `summarize`: Create a summary string describing the text

3. Build the graph with sequential edges:
   - `START` → `clean_text` → `analyze_text` → `summarize` → `END`

### Acceptance Criteria
- [ ] All three nodes execute in order
- [ ] Each node correctly transforms state
- [ ] Final state contains all fields populated
- [ ] Test with: `{"text": "  Hello   WORLD  this is    a TEST  "}`

### Hints
- Each node should return a dict with only the fields it updates
- The state accumulates updates from each node

---

## Task 3: Conditional Routing
> **Pattern**: Router (Conditional Branching)
> **Type**: Flow Engineering

### Objective  
Build a graph that routes to different nodes based on a condition.

### Requirements
1. Create a `State` with:
   - `number: int` - input number
   - `result: str` - the result message
   - `path_taken: str` - which path was used

2. Create three nodes:
   - `check_number`: Examines the number (doesn't modify state, used for routing)
   - `handle_even`: Sets result to "Even number: {number}"
   - `handle_odd`: Sets result to "Odd number: {number}"

3. Create a routing function that returns `"handle_even"` or `"handle_odd"`

4. Build the graph:
   - `START` → conditional edge using your routing function
   - Both `handle_even` and `handle_odd` → `END`

### Acceptance Criteria
- [ ] `{"number": 4}` routes to `handle_even`
- [ ] `{"number": 7}` routes to `handle_odd`
- [ ] `path_taken` field correctly indicates which path was used
- [ ] Use `add_conditional_edges()` method

### Hints
- Conditional edge function signature: `def router(state: State) -> str`
- Return the name of the next node as a string

---

# 🟡 Level 2: Intermediate

## Task 4: LLM Integration
> **Pattern**: Simple Chain with LLM
> **Type**: Cognitive Architecture

### Objective
Integrate an LLM into your graph to generate responses.

### Requirements
1. Setup:
   - Use `langchain.chat_models.init_chat_model()` 
   - Use any model you have access to (OpenAI, Anthropic, etc.)

2. Create a `State` with:
   - `topic: str` - the topic to write about
   - `draft: str` - first draft
   - `final: str` - polished version

3. Create two nodes:
   - `generate_draft`: LLM writes first draft about the topic
   - `polish_draft`: LLM improves the draft

4. Build: `START` → `generate_draft` → `polish_draft` → `END`

### Acceptance Criteria
- [ ] LLM is properly initialized and called
- [ ] Both nodes successfully invoke the LLM
- [ ] Final output shows improvement from draft to final
- [ ] Test with: `{"topic": "the benefits of morning walks"}`

### Hints
- Use `llm.invoke(prompt)` to call the LLM
- Access `msg.content` to get the string response
- Handle environment variables for API keys

---

## Task 5: Tool-Calling Agent
> **Pattern**: ReAct Agent (Reasoning + Acting)
> **Type**: Agentic Loop

### Objective
Build an agent that can use tools to answer questions.

### Requirements
1. Create tools using `@tool` decorator:
   - `add(a: int, b: int)`: Returns sum
   - `multiply(a: int, b: int)`: Returns product
   - `subtract(a: int, b: int)`: Returns difference

2. Use `MessagesState` (built-in state with messages list)

3. Create nodes:
   - `llm_call`: Invokes LLM with tools bound
   - `tool_node`: Executes tool calls from LLM response

4. Create conditional routing:
   - If LLM made tool calls → go to `tool_node`
   - If no tool calls → go to `END`
   - After `tool_node` → back to `llm_call` (creates a loop!)

### Acceptance Criteria
- [ ] Agent correctly answers: "What is 5 + 3?"
- [ ] Agent correctly answers: "What is 7 * 6?"
- [ ] Agent handles multi-step: "Add 10 and 5, then multiply by 2"
- [ ] Agent stops when no more tool calls needed

### Hints
- Use `model.bind_tools(tools)` to give LLM access to tools
- Check `last_message.tool_calls` to see if LLM wants to use tools
- Use `ToolMessage` to send tool results back

---

## Task 6: Prompt Chaining with Gates
> **Pattern**: Self-Correcting Agent (Evaluator-Optimizer)
> **Type**: Reflection Loop

### Objective
Build a content generation pipeline with quality gates.

### Requirements
1. Create a `State` with:
   - `topic: str`
   - `outline: str`
   - `content: str`
   - `quality_score: int`
   - `revision_count: int`
   - `final_content: str`

2. Create nodes:
   - `create_outline`: LLM generates an outline
   - `write_content`: LLM writes content from outline  
   - `evaluate_quality`: LLM scores content 1-10
   - `revise_content`: LLM improves content
   - `finalize`: Copies content to final_content

3. Routing logic:
   - After `evaluate_quality`:
     - If score >= 7 → `finalize`
     - If score < 7 AND revision_count < 3 → `revise_content`
     - If score < 7 AND revision_count >= 3 → `finalize` (give up)
   - After `revise_content` → back to `evaluate_quality`

### Acceptance Criteria
- [ ] Pipeline creates outline → content → evaluation
- [ ] Low scores trigger revision loop
- [ ] Maximum 3 revisions before forcing finalize
- [ ] Print revision count and final quality score

### Hints
- Parse the quality score from LLM response (ask for just a number)
- Increment `revision_count` in the `revise_content` node
- Use multiple return values in conditional edge routing

---

# 🟠 Level 3: Advanced

## Task 7: Stateful Conversations with Memory
> **Pattern**: Persistent Chatbot
> **Type**: Memory Management

### Objective
Build a chatbot that remembers conversation history.

### Requirements
1. Use `MessagesState` with `Annotated[list, operator.add]` for message accumulation

2. Create a chatbot node that:
   - Takes full message history
   - Generates contextual responses
   - Appends new messages to state

3. Implement using **checkpointing**:
   - Use `MemorySaver` for persistence
   - Use `thread_id` to maintain separate conversations

4. Test multi-turn conversations:
   - "My name is Bob"
   - "What's my name?"
   - "Tell me a joke about my name"

### Acceptance Criteria
- [ ] Bot remembers information from previous turns
- [ ] Different thread_ids have isolated memories
- [ ] Conversation history is preserved and accessible
- [ ] Implement `config={"configurable": {"thread_id": "1"}}`

### Hints
- `from langgraph.checkpoint.memory import MemorySaver`
- `graph.compile(checkpointer=MemorySaver())`
- Pass config when invoking: `graph.invoke(input, config)`

### Documentation
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Memory](https://docs.langchain.com/oss/python/langgraph/add-memory)

---

## Task 8: Human-in-the-Loop Approval
> **Pattern**: Human-in-the-Loop (HITL)
> **Type**: Cognitive Architecture

### Objective
Build a workflow that pauses for human approval before taking actions.

### Requirements
1. Create an "email sender" workflow with `State`:
   - `recipient: str`
   - `subject: str`
   - `draft: str`
   - `approved: bool`
   - `sent: bool`

2. Create nodes:
   - `draft_email`: LLM writes email draft
   - `send_email`: Simulates sending (just print + set sent=True)

3. Implement **interrupt before** the `send_email` node:
   - Graph pauses after drafting
   - Human can review and approve
   - Resume with modified state if needed

4. Flow:
   - `START` → `draft_email` → (interrupt) → `send_email` → `END`

### Acceptance Criteria
- [ ] Graph pauses after drafting
- [ ] Can inspect the draft before sending
- [ ] Can modify the draft and resume
- [ ] After approval, email is "sent"

### Hints
- Use `interrupt_before=["send_email"]` in compile()
- Use `graph.get_state(config)` to see current state
- Use `graph.update_state(config, new_values)` to modify
- Use `graph.invoke(None, config)` to resume

### Documentation
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)

---

## Task 9: Parallel Execution
> **Pattern**: Parallelization (Map-Reduce style)
> **Type**: Flow Engineering

### Objective
Build a graph that executes multiple branches in parallel.

### Requirements
1. Create a "research assistant" that gathers info from multiple sources:
   - `State` with: `query: str`, `web_results: str`, `academic_results: str`, `news_results: str`, `combined: str`

2. Create parallel nodes (simulate with sleep + mock data):
   - `search_web`: Simulates web search (sleep 1s)
   - `search_academic`: Simulates academic search (sleep 1.5s)  
   - `search_news`: Simulates news search (sleep 0.5s)
   - `combine_results`: Merges all results

3. Build graph with fan-out/fan-in:
   - `START` → all three search nodes (parallel)
   - All search nodes → `combine_results`
   - `combine_results` → `END`

### Acceptance Criteria
- [ ] All three searches run in parallel (total time ~1.5s not 3s)
- [ ] Results from all branches are combined
- [ ] Use timing to verify parallel execution
- [ ] Each search node independently updates its state field

### Hints
- Add multiple edges from START: one to each search node
- The `combine_results` node receives state after ALL parallel nodes complete
- Use `time.sleep()` and measure total execution time

### Documentation
- [Parallelization](https://docs.langchain.com/oss/python/langgraph/workflows-agents#parallelization)

---

# 🔴 Level 4: Expert

## Task 10: Subgraphs
> **Pattern**: Hierarchical Graph
> **Type**: Modular Architecture

### Objective
Build a modular system using subgraphs for code reuse.

### Requirements
1. Create a **research subgraph**:
   - Nodes: `search` → `summarize` → `validate`
   - Own state type with research-specific fields

2. Create a **writing subgraph**:
   - Nodes: `outline` → `draft` → `edit`
   - Own state type with writing-specific fields

3. Create a **parent graph** that:
   - Accepts a topic
   - Calls research subgraph
   - Passes results to writing subgraph
   - Returns final article

4. Handle state transformation between graphs

### Acceptance Criteria
- [ ] Subgraphs compile independently
- [ ] Parent graph successfully orchestrates both
- [ ] State properly transforms between graph boundaries
- [ ] Final output is a researched article

### Hints
- Compile subgraphs first: `research_graph = research_builder.compile()`
- Add compiled graph as node: `parent.add_node("research", research_graph)`
- May need state transformation functions

### Documentation
- [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

---

## Task 11: Multi-Agent Orchestration
> **Pattern**: Supervisor / Orchestrator
> **Type**: Multi-Agent System

### Objective
Build a supervisor that coordinates multiple specialized agents.

### Requirements
1. Create specialized agents:
   - **Researcher**: Has web search tools
   - **Analyst**: Has calculation tools
   - **Writer**: Has no tools, just writes

2. Create a **Supervisor** agent that:
   - Receives the task
   - Decides which agent to delegate to
   - Routes to appropriate agent
   - Collects results
   - Decides if more work needed or complete

3. Implement routing:
   - Supervisor → (researcher | analyst | writer | END)
   - Each agent → back to Supervisor

### Acceptance Criteria
- [ ] Supervisor correctly identifies which agent to use
- [ ] Complex tasks use multiple agents in sequence
- [ ] Results flow back through supervisor
- [ ] Test: "Research the population of Tokyo, calculate growth rate, write a summary"

### Hints
- Supervisor is an LLM that returns which agent to call next
- Each agent is its own compiled subgraph
- Use structured output for supervisor decisions

### Documentation
- [Multi-agent](https://docs.langchain.com/oss/python/langgraph/workflows-agents#orchestrator-worker)

---

## Task 12: Production-Ready Agent
> **Pattern**: Production Agent
> **Type**: Reliability Engineering

### Objective
Build a complete, production-ready agent with all best practices.

### Requirements
1. **Durable Execution**:
   - Use checkpointing for fault tolerance
   - Handle retries gracefully
   - Implement timeout limits

2. **Streaming**:
   - Stream tokens as they're generated
   - Implement `astream_events`

3. **Observability**:
   - Add clear logging
   - Track token usage
   - Measure latency

4. **Error Handling**:
   - Graceful tool failures
   - Max iterations limit
   - Fallback responses

5. **Testing**:
   - Unit test each node independently
   - Integration test the full graph

### Acceptance Criteria
- [ ] Agent recovers from simulated failures
- [ ] Streaming works end-to-end
- [ ] Logs show clear execution trace
- [ ] Has max iteration safeguard (prevent infinite loops)
- [ ] Includes at least 3 unit tests

### Hints
- Wrap tool calls in try/except
- Use `RetryPolicy` for automatic retries
- `for event in graph.stream(input): print(event)`

### Documentation
- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
- [Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [Testing](https://docs.langchain.com/oss/python/langgraph/test)

---

## Task 13: Cross-Thread Persistence (Store)
> **Pattern**: Personal Assistant
> **Type**: Long-term Memory

### Objective
Build an assistant that remembers user information across *different* conversation threads using a Store.

### Requirements
1. **Setup Store**:
   - Use `InMemoryStore`
   - Pass it to `compile(store=...)`

2. **Define Schema**:
   - Create a `UserProfile` Pydantic model (e.g., name, preferences)

3. **Memory Node**:
   - Create a node that extracts user info from conversation
   - Save it to the store using `store.put()`
   - Scope it by `user_id` (not `thread_id`)

4. **Response Node**:
   - Retrieve user info using `store.get()`
   - Generate response personalized with that info

5. **Test Scenario**:
   - Thread A: "I am vegan." (Bot saves this)
   - Thread B (New Thread): "Suggest a lunch place." (Bot suggests vegan option)

### Acceptance Criteria
- [ ] Information persists across two completely different `thread_id`s
- [ ] `store.put()` correctly saves data under a user namespace
- [ ] `store.get()` correctly retrieves data in a new session
- [ ] Assistant uses retrieved info to personalize response

### Hints
- Use `config["configurable"]["user_id"]` to namespace data
- `store.put(("user", user_id), "profile", {"diet": "vegan"})`
- `store.get(("user", user_id), "profile")`

---

# 📝 How to Use This Curriculum

## For Each Task:
1. **Read the spec** thoroughly
2. **Create a new file**: `task_XX_name.py`
3. **Implement** the solution
4. **Verify** against acceptance criteria
5. **Ask for review** when stuck or complete

## Getting Help:
- Share your code and I'll provide feedback
- Ask clarifying questions about requirements
- Request hints if stuck (but try first!)

## Progress Tracking:
Mark your progress here:

| Task | Status | Notes |
|------|--------|-------|
| Task 1 | [x] Completed | |
| Task 2 | [x] Completed | |
| Task 3 | [x] Completed | |
| Task 4 | [x] Completed | |
| Task 5 | [x] Completed | |
| Task 6 | [x] Completed | Worked via short-circuit (score 9), missing init fix |
| Task 7 | [x] Completed | |
| Task 8 | [x] Completed | |
| Task 9 | [x] Completed | Parallel fan-out/fan-in, 1.5s execution |
| Task 10 | [x] Completed | Subgraphs with state transformation |
| Task 11 | ⬜ Not Started | |
| Task 12 | ⬜ Not Started | |
| Task 13 | ⬜ Not Started | |

---

**Ready to start? Begin with Task 1!** 🚀
