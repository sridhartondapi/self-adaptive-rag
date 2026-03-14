from langchain_community.vectorstores import Chroma
from retrieval.agents.clients.embeddings import get_embeddings
from retrieval.agents.config.settings import VECTORSTORE_PATH, COLLECTION_NAME

def get_vectorstore():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=str(VECTORSTORE_PATH),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )