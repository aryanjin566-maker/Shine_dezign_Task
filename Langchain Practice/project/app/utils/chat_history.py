from langchain_core.messages import (
    SystemMessage
)

chat_history = [

    SystemMessage(
        content="""
        You are AI website assistant.
        Answer using scraped website data.
        """
    )

]