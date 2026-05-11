import os
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool

# 1. SETUP LLM & TOOLS
llm = ChatOpenAI(model="gpt-4o", temperature=0)

search_tools = [DuckDuckGoSearchRun(), WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()), ArxivQueryRun()]
code_tools = [PythonREPLTool()]

# 2. AGENT CREATOR FUNCTION (Modern Approach)
def create_specialized_agent(llm, tools, system_message):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# 3. INITIALIZE SPECIALISTS
researcher = create_specialized_agent(llm, search_tools, "You find facts and papers.")
coder = create_specialized_agent(llm, code_tools, "You write and run Python code.")

# 4. THE SUPERVISOR (The Decision Maker)
# We define the team members
members = ["Researcher", "Coder"]
system_prompt = (
    "You are a supervisor managing a team: {members}. "
    "Based on the user request, decide who should act next. "
    "If you have the final answer, respond with FINISH."
)

options = ["FINISH"] + members
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}"),
]).partial(options=str(options), members=", ".join(members))

# 5. EXECUTION LOGIC (The Router)
def run_team(user_query: str):
    messages = [HumanMessage(content=user_query)]
    
    # --- Step 1: Supervisor Decides ---
    # In a full LangGraph setup, this is a loop. Here is the direct logic:
    supervisor_decision = (prompt | llm).invoke({"messages": messages})
    next_agent = supervisor_decision.content # The AI picks 'Researcher' or 'Coder'
    
    print(f"\n[SUPERVISOR]: I think the {next_agent} should handle this.\n")

    # --- Step 2: Selected Agent Acts ---
    if "Researcher" in next_agent:
        result = researcher.invoke({"messages": messages})
    elif "Coder" in next_agent:
        result = coder.invoke({"messages": messages})
    else:
        print("Supervisor decided to FINISH.")
        return

    print(f"\n[FINAL RESULT]: {result['output']}")

# 6. TEST THE DECISION MAKING
print("--- TEST 1: RESEARCH ---")
run_team("Who won the Nobel Prize in Physics 2023?")

print("\n--- TEST 2: CODING ---")
run_team("Calculate the square root of 576 using Python.")