from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([
    ('system', 'you are {domain} expert'),
    ('human', 'what is {query}?')
])

prompt = chat_template.invoke({
    'domain': 'AI',
    'query': 'LLM'
})
print(prompt)