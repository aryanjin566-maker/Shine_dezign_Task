from langchain_community.document_loaders import WebBaseLoader

from langchain_groq import ChatGroq

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def scrape_website(url):

    print("\n[SCRAPING WEBSITE...]\n")

    loader = WebBaseLoader(url)

    docs = loader.load()

    return docs[0].page_content

llm = ChatGroq(
    groq_api_key="your_groq_api_key_here",
    model="llama-3.1-8b-instant",
    temperature=0.3,
    max_tokens=2048
)

url = "https://python.langchain.com"

scraped_data = scrape_website(url)


# -----------------------------------
# CHAT HISTORY
# -----------------------------------

chat_history = [

    SystemMessage(
        content="""
        You are an AI website assistant.

        Your job is to answer user questions
        using the scraped website data.

        Give short and clear answers.
        """
    )
]

while True:

    user_question = input("\nYou: ")

    # Exit condition
    if user_question.lower() in ["exit", "quit"]:
        print("\nChat Ended.")
        break

    human_message = HumanMessage(
        content=f"""
        User Question:
        {user_question}

        Scraped Website Data:
        {scraped_data[:4000]}
        """
    )
    chat_history.append(human_message)

    print("\n[CHAT HISTORY]\n")
    for msg in chat_history:
        if isinstance(msg, SystemMessage):
            print(f"SYSTEM: {msg.content[:100]}")
        elif isinstance(msg, HumanMessage):
            print(f"HUMAN: {msg.content[:100]}")
        elif isinstance(msg, AIMessage):
            print(f"ASSISTANT: {msg.content[:100]}")

    response = llm.invoke(chat_history)

    ai_message = AIMessage(content=response.content)

    chat_history.append(ai_message)

    print("\nAssistant:\n")
    print(response.content)
    print(scraped_data[:4000])