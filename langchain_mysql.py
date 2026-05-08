from langchain.tools import tool
from langchain.agents import initialize_agent , AgentType
from langchain.chat_models import chatOllama
import os 
from langchain.chat_models import SQLDatabase
from sqlalchemy import create_engine

MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"  
MYSQL_PORT = "3306"
MYSQL_DB = "LANGCHAIN_DB" 

mysql_url = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

db = SQLDatabase.from_uri(mysql_url)

model = "llama3.2"
llm = chatOllama(model=model ,streaming = True)

sql_tool = tool(
  name = "SQL query Executor",
  func = db.run,
  description = "Exceute SQL queries and retrieve result from MYSQL database"
)

query = "select * from users"
result = sql_tool.run(query)
print(result)
