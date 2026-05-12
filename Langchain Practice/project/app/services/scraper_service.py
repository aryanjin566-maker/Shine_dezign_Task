from langchain_community.document_loaders import WebBaseLoader


def scrape_website(url: str):

    loader = WebBaseLoader(url)

    docs = loader.load()

    return docs[0].page_content