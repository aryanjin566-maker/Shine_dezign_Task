from fastapi import APIRouter

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from app.models.chat_model import ChatRequest

from app.services.scraper_service import (
    scrape_website
)

from app.services.llm_service import (
    get_llm
)

from app.utils.chat_history import (
    chat_history
)

router = APIRouter()

llm = get_llm()


@router.post("/chat")

def chat(data: ChatRequest):

    scraped_data = scrape_website(data.url)

    human_message = HumanMessage(
        content=f"""
        User Question:
        {data.question}

        Scraped Website Data:
        {scraped_data[:4000]}
        """
    )

    chat_history.append(human_message)

    response = llm.invoke(chat_history)

    ai_message = AIMessage(
        content=response.content
    )

    chat_history.append(ai_message)

    return {
        "response": response.content
    }