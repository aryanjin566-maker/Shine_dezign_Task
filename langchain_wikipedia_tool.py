import os 
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.chat_models import chatOllama
from langchain.tools import wikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper

model = "llama3.2"
llm = chatOllama(model=model)
wiki = wikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

wiki_tool = Tool(
  name = "wikipedia search",
  func = wiki.run,
  description = "useful for seraching Wikipedia arcticles"
)

tools = [wiki_tool]

agent = initialize_agent(
  tools = tools,
  llm =llm ,
  agent = AgentType.ZERO_SHOT_REACT_DISCRIPTIONS,
  verbose = True ,
  handle_prasing_errors = True
)

response = agent.run("Tell me about Langchain")
print(response)


